import streamlit as st
import re
from streamlit_hub.manager.manager import Manager
from streamlit_hub.models.App import LocalApp, RepoApp


def local_source(manager: Manager, app_name: str, run_by_default: bool):
    app_path = st.text_input("App Path:")

    if st.button("Register"):
        _register_new_local_project(manager, app_name, run_by_default, app_path)


def new_local_source(manager: Manager, app_name: str, run_by_default: bool):
    if st.button("Register"):
        app_path = manager.app_access.create_new_local_app_project(app_name)
        if _register_new_local_project(manager, app_name, run_by_default, app_path, True):
            st.success('You can start editing your code in the "Edit your App" tab')


def _register_new_local_project(
    manager: Manager, app_name: str, run_by_default: bool, app_path: str, app_managed=False
) -> bool:
    if app_name and app_path:
        ret = manager.register_app(
            LocalApp(name=app_name, run_by_default=run_by_default, path=app_path, app_managed=app_managed)
        )
        if ret:
            st.error(ret)
        else:
            st.success(f"App {app_name} registered successfully!")
            return True
    else:
        st.error("Please provide both App Name and App Path.")
    return False


def repo_source(manager: Manager, app_name: str, run_by_default: bool):
    repo_url = st.text_input("Repo URL:")
    repo_branch = st.text_input("Repo Branch:")
    path_in_repo = st.text_input("Path of streamlit entrypoint in Repo:")

    if re.match(r"[a-zA-z-]*", app_name) is None:
        st.warning("The application name must only be compoased of letter and hyphens -")

    if st.button("Register"):
        if app_name and repo_url and repo_branch and path_in_repo:
            ret = manager.register_app(
                RepoApp(
                    name=app_name,
                    run_by_default=run_by_default,
                    repo_url=repo_url,
                    branch=repo_branch,
                    streamlit_entry_point_in_repo=path_in_repo,
                )
            )
            if ret:
                st.error(ret)
            else:
                st.success(f"App {app_name} registered successfully!")
        else:
            st.error("Please provide both App Name, Repo URL, Report branch, and Path in Repo")


def show_register(manager: Manager):
    st.header("Register New App")

    app_name = st.text_input("App Name:")
    run_by_default = st.checkbox("Run application at startup")

    source = st.radio("Source of application", ["New Local Application", "Existing Local Application", "Git Repo"])

    if source == "Existing Local Application":
        local_source(manager, app_name, run_by_default)
    elif source == "New Local Application":
        new_local_source(manager, app_name, run_by_default)
    else:
        repo_source(manager, app_name, run_by_default)
