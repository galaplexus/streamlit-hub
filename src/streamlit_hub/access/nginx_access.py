import logging
import re
import os
import configparser
import platform
import subprocess
from typing import Optional
import nginx


logger = logging.getLogger(__name__)


class NginxAccess:
    """
    Accesses configuration on ngix server.
    The server is used to route path from the common url to the dedicated streamlit application.

    The access manages:
        - an nginx.ini file which handles the current nginx configuration
        - a nginx configuration which is managed to route the requests to the streamlit applications
        - the nginx serice itself (restart when needed)
    """

    persisited_base_path = os.path.join(os.path.expanduser("~"), ".streamlit-hub")
    persisited_nginx_config_path = os.path.join(persisited_base_path, "nginx.ini")
    config: configparser.ConfigParser
    nginx_conf: Optional[nginx.Conf] = None
    path_key = "config_path"
    port_key = "serving_port"
    enabled_key = "enabled"

    def __init__(self) -> None:
        if not os.path.exists(self.persisited_base_path):
            os.makedirs(self.persisited_base_path)
        if not os.path.exists(self.persisited_nginx_config_path):
            with open(self.persisited_nginx_config_path, "w") as file:
                config = configparser.ConfigParser()
                config["DEFAULT"] = {}
                config.write(file)
        self.config = configparser.ConfigParser()
        self.config.read(self.persisited_nginx_config_path)
        self.nginx_conf = self._parse_conf()

    def restart_nginx(self):
        if not self.get_enabled_flag():
            return
        if platform.system() == "Windows":
            subprocess.run(["nginx", "-s", "reload"], check=True)
        else:
            subprocess.run(["sudo", "systemctl", "reload", "nginx"], check=True)

    def add_app(self, name: str, port: int):
        if re.search(r"\s", name):
            raise Exception("The application name cannot contain white spaces")

        if self.contains_app(name):
            return
        if self.contains_port(port):
            raise Exception("The name of the application or the port was already in use.")
        new_location = nginx.Location(f"/{name}")
        new_location.add(nginx.Key("proxy_pass", f"http://localhost:{port}/{name}"))
        new_location.add(nginx.Key("proxy_set_header", "Host $host"))
        new_location.add(nginx.Key("proxy_set_header", "X-Real-IP $remote_addr"))
        new_location.add(nginx.Key("proxy_set_header", "X-Forwarded-For $proxy_add_x_forwarded_for"))
        new_location.add(nginx.Key("proxy_set_header", "X-Forwarded-Proto $scheme"))
        new_location.add(nginx.Key("proxy_buffering", "off"))
        new_location.add(nginx.Key("proxy_http_version", "1.1"))
        new_location.add(nginx.Key("proxy_set_header", "Upgrade $http_upgrade"))
        new_location.add(nginx.Key("proxy_set_header", 'Connection "upgrade"'))
        new_location.add(nginx.Key("proxy_read_timeout", "86400"))
        for child in self.nginx_conf.children:
            child.add(new_location)
        self._write_conf_to_file()

    def contains_app(self, name) -> bool:
        for k in self.nginx_conf.children:
            for c in k.children:
                if type(c) is not nginx.Location:
                    continue
                c: nginx.Location
                if c.value == "/" + name:
                    return True
        return False

    def contains_port(self, port: int) -> bool:
        for k in self.nginx_conf.children:
            for c in k.children:
                if type(c) is not nginx.Location:
                    continue
                c: nginx.Location
                for vals in c.children:
                    vals: nginx.Key
                    if type(vals) is not nginx.Key:
                        continue
                    if vals.value.startswith(f"http://localhost:{port}/"):
                        return True
        return False

    def _parse_conf(self) -> Optional[nginx.Conf]:
        config_path = self.get_config_path()
        if not config_path:
            logger.warn("No config path found for the nginx conf file")
            return None
        if os.path.exists(config_path):
            self.nginx_conf = nginx.loadf(config_path)
        else:
            self.nginx_conf = nginx.Conf()
            base_server = nginx.Server()
            base_server.add(nginx.Key("listen", str(self.get_serving_port())))
            base_server.add(nginx.Key("server_name", "localhost"))
            self.nginx_conf.add(base_server)
            self.add_app("hub", 8501)
        return self.nginx_conf

    def _write_conf_to_file(self):
        nginx.dumpf(self.nginx_conf, self.get_config_path())

    def get_config_path(self) -> Optional[str]:
        return self.config["DEFAULT"][self.path_key] if self.path_key in self.config["DEFAULT"] else None

    def set_config_path(self, directory: str):
        if self.get_config_path() == directory:
            return
        self.config["DEFAULT"][self.path_key] = directory
        with open(self.persisited_nginx_config_path, "w") as f:
            self.config.write(f)

    def get_serving_port(self) -> int:
        return int(self.config["DEFAULT"][self.port_key]) if self.port_key in self.config["DEFAULT"] else 8080

    def set_serving_port(self, port: int):
        if self.get_serving_port() == port:
            return
        self.config["DEFAULT"][self.port_key] = str(port)
        with open(self.persisited_nginx_config_path, "w") as f:
            self.config.write(f)

    def get_enabled_flag(self) -> bool:
        return bool(self.config["DEFAULT"][self.enabled_key]) if self.enabled_key in self.config["DEFAULT"] else False

    def set_enabled_flag(self, enabled: bool):
        if self.get_enabled_flag() == enabled:
            return
        self.config["DEFAULT"][self.enabled_key] = str(enabled)
        with open(self.persisited_nginx_config_path, "w") as f:
            self.config.write(f)

    def toggle_enabled_flag(self):
        f = self.get_enabled_flag()
        self.config["DEFAULT"][self.enabled_key] = str(not f)
        with open(self.persisited_nginx_config_path, "w") as f:
            self.config.write(f)
