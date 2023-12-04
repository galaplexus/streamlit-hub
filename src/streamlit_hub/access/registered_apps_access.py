import json
import os
from typing import List
from streamlit_hub.models.App import App, LocalApp, RepoApp


class AppAccess:
    persisited_base_path = os.path.join(os.path.expanduser("~"), ".streamlit-hub")
    persisited_registered_apps_path = os.path.join(persisited_base_path, "registered_apps.json")

    def __init__(self) -> None:
        if not os.path.exists(self.persisited_base_path):
            os.makedirs(self.persisited_base_path)
        if not os.path.exists(self.persisited_registered_apps_path):
            with open(self.persisited_registered_apps_path, "w") as file:
                json.dump([], file)
        pass

    def get_list(self) -> List[App]:
        ret = []
        with open(self.persisited_registered_apps_path, "r") as file:
            db = json.load(file)
            for app in db:
                if "branch" in app and "streamlit_entry_point_in_repo" in app and "repo_url" in app:
                    ret.append(
                        RepoApp(
                            app["name"],
                            run_by_default=app["default_on"] if "default_on" in app else False,
                            repo_url=app["repo_url"],
                            branch=app["branch"],
                            streamlit_entry_point_in_repo=app["streamlit_entry_point_in_repo"],
                            desired_port=app["desired_port"] if "desired_port" in app else None,
                        )
                    )
                elif "path" in app:
                    ret.append(
                        LocalApp(
                            app["name"],
                            run_by_default=app["default_on"] if "default_on" in app else False,
                            path=app["path"],
                            desired_port=app["desired_port"] if "desired_port" in app else None,
                        )
                    )
                else:
                    raise Exception(f"Could not parse {app} into an App")
        return ret

    def persist_list(self, apps: List[App]):
        encoded = []
        for app in apps:
            new = {"name": app.name, "default_on": app.run_by_default}
            if app.desired_port:
                new["desired_port"] = app.desired_port
            if type(app) is LocalApp:
                new["path"] = app.path
            if type(app) is RepoApp:
                new["branch"] = app.branch
                new["streamlit_entry_point_in_repo"] = app.streamlit_entry_point_in_repo
                new["repo_url"] = app.repo_url
            encoded.append(new)
        with open(self.persisited_registered_apps_path, "w") as file:
            json.dump(encoded, file)
