import os
import subprocess
import logging
import threading
import time
from typing import List, Optional
from streamlit_hub.access.registered_apps_access import AppAccess
from streamlit_hub.access.repo_access import RepoAccess
from streamlit_hub.models.App import App, LocalApp, RepoApp

from streamlit_hub.models.RunningProcess import LocalProcess

logger = logging.getLogger(__name__)


class Manager:
    registered_apps: List[App] = []
    app_access = AppAccess()
    occupied_ports: set[int] = set()

    def __init__(self) -> None:
        self.registered_apps = self.app_access.get_list()
        for app in self.registered_apps:
            if app.run_by_default:
                try:
                    self.start_app(app)
                except:
                    logger.error(f"couldnt start {app.name} at startup")
        check_thread = threading.Thread(target=self._clean_closed_processes, args=(), daemon=True)
        check_thread.start()

    def start_app(self, app: App):
        logger.info(f"Starting {app}")
        port = int(app.desired_port) if app.desired_port is not None else self._find_next_port()
        if type(app) is LocalApp:
            path = app.path
        elif type(app) is RepoApp:
            if not app.local_path:
                app.local_path = os.path.join(RepoAccess(app).repo_path, app.streamlit_entry_point_in_repo)
            path = app.local_path
        else:
            logger.error("We can't process other type of app than local apps at the moment")
            return None
        process = subprocess.Popen(
            ["python", "-m", "streamlit", "run", path, "--server.port", str(port)], start_new_session=True
        )
        self.occupied_ports.add(port)
        app.running_process = LocalProcess("", port, process)
        return process

    def register_app(self, app: App) -> Optional[str]:
        if any(map(lambda x: x.name == app.name, self.registered_apps)):
            return "An app with the same name was already added"
        if type(app) is RepoApp:
            access = RepoAccess(app)
            app.local_path = os.path.join(access.repo_path, app.streamlit_entry_point_in_repo)
        self.registered_apps.append(app)
        self.app_access.persist_list(self.registered_apps)

    def toggle_run_default_app(self, app: App, run_by_default: bool) -> Optional[str]:
        app.run_by_default = run_by_default
        self.app_access.persist_list(self.registered_apps)

    def unregister_app(self, app: App) -> Optional[str]:
        self.registered_apps = list(filter(lambda matching_app: app.name != matching_app.name, self.registered_apps))
        self.app_access.persist_list(self.registered_apps)

    def stop_app(self, app: App) -> subprocess.Popen:
        logger.info(f"Stopping {app.name}")
        if app.running_process is None:
            logger.info(f"{app.name} was alreay stopped")
            return
        local_process = app.running_process
        local_process: LocalProcess
        process = local_process.process
        try:
            process.terminate()
            process.wait(timeout=5)  # Wait for the process to finish
            logger.info(f"{app.name} was stopped")
        except subprocess.TimeoutExpired:
            process.kill()  # If terminate() doesn't work, forcefully kill the process
            logger.info(f"{app.name} was forced stopped")
        if local_process.port in self.occupied_ports:
            self.occupied_ports.remove(local_process.port)
        app.running_process = None

    def start_all(self):
        # Start Streamlit processes for each app
        for app in self.registered_apps:
            self.start_app(app)

    def end_all(self):
        for app in self.registered_apps:
            self.stop_app(app)

    def refresh_app(self, app):
        if type(app) is RepoApp:
            access = RepoAccess(app)
            access.pull()

    def _find_next_port(self) -> int:
        for potential in range(8503, 8550):
            if potential in self.occupied_ports:
                continue
            if any(map(lambda x: x.desired_port == potential, self.registered_apps)):
                continue
            return potential
        raise Exception("No new port found")

    def _clean_closed_processes(self):
        while True:
            for app in self.registered_apps:
                if (
                    app.running_process
                    and type(app.running_process) is LocalProcess
                    and app.running_process.process.poll() is not None
                ):
                    logger.warn(f"Process of app '{app.name}' has finished without commanding its closure.")
                    port = app.running_process.port
                    if port in self.occupied_ports:
                        self.occupied_ports.remove(port)
                    app.running_process = None

            time.sleep(1)  # Check every second
