import os
import subprocess
from typing import Optional
from streamlit_hub.models.App import RepoApp


class RepoAccess:
    base_path = os.path.join(os.path.expanduser("~"), ".streamlit-hub", "repos")
    repo_name: str
    repo_path: str

    def __init__(self, app: RepoApp):
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
        self.app = app
        self.repo_name = app.repo_url.split("/")[-1].replace(".git", "")
        self.repo_path = os.path.join(self.base_path, self.repo_name)
        RepoAccess.clone_repo(app.repo_url, self.repo_path)
        self.checkout_branch(app.branch)

    @staticmethod
    def clone_repo(url, destination):
        if not RepoAccess._is_git_initialized(destination):
            os.makedirs(destination)
            # Clone the repository if it doesn't exist
            subprocess.run(["git", "clone", url, destination])

    def checkout_branch(self, branch: str):
        os.chdir(self.repo_path)
        subprocess.run(["git", "checkout", branch])

    def pull(self, branch: Optional[str] = None):
        if branch is not None:
            self.checkout_branch(branch)
        os.chdir(self.repo_path)
        subprocess.run(["git", "pull"])

    @staticmethod
    def _is_git_initialized(directory):
        return os.path.exists(os.path.join(directory, ".git"))
