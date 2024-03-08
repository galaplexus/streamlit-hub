import dataclasses
import os
from typing import Optional
from streamlit_hub.models.RunningProcess import RunningProcess


@dataclasses.dataclass
class App:
    name: str
    run_by_default: bool
    running_process: Optional[RunningProcess] = None
    desired_port: Optional[str] = None

    def cleanup(self):
        pass


@dataclasses.dataclass
class LocalApp(App):
    path: str = ""
    app_managed: bool = False

    def cleanup(self):
        if self.app_managed:
            os.remove(self.path)


@dataclasses.dataclass
class RepoApp(App):
    repo_url: str = ""
    local_path: str = ""
    streamlit_entry_point_in_repo: str = ""
    branch: str = ""
