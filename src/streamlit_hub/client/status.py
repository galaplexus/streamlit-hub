from streamlit_hub.manager.manager import Manager
import streamlit as st

from streamlit_hub.models.App import LocalApp, RepoApp


def show_status(manager: Manager):
    col1, col2, col3 = st.columns([1, 1, 1])
    col1.write("**App Name**")
    col2.write("**App Details**")
    col3.write("**Actions**")
    for app in manager.registered_apps:
        st.markdown("""---""")
        (
            col1,
            col2,
            col3,
        ) = st.columns([0.2, 1, 1])
        col1.write(f"**{app.name}**")
        if type(app) is LocalApp:
            col2.write(app.path)
        if type(app) is RepoApp:
            col2.write(f"**url:** {app.repo_url}, **branch:** {app.branch}")
        if app.running_process is None:
            col3.button("Start", on_click=manager.start_app, args=(app,), key=("start", app))
        else:
            col3.button("Stop", on_click=manager.stop_app, args=(app,), key=("start", app))

        col3.checkbox(
            "Run at startup",
            value=app.run_by_default,
            on_change=manager.toggle_run_default_app,
            args=(app, not app.run_by_default),
            key=("toggle_default", app),
        )
        if type(app) is RepoApp:
            col3.button("Pull Latest", on_click=manager.refresh_app, args=(app,), key=("refresh", app))

        col3.button("Delete", on_click=manager.unregister_app, args=(app,), key=("Delete", app))
    st.markdown("""---""")
