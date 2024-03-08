from typing import List
import streamlit as st
from streamlit_hub.manager.manager import Manager
from streamlit_hub.models.App import LocalApp


def edit_local_app(manager: Manager):
    st.header("Edit your App")
    local_apps: List[LocalApp] = list(filter(lambda x: type(x) is LocalApp, manager.app_access.get_list()))
    if not local_apps:
        st.warning("There are no local app to edit. Please register one in Register tab")
        return
    local_apps_names = map(lambda x: x.name, local_apps)
    selection = st.sidebar.selectbox("App to Edit", local_apps_names)

    if selection:
        app: LocalApp = list(filter(lambda x: x.name == selection, local_apps))[0]
        with open(app.path, "r") as f:
            code = f.read()
        new_code = st.text_area("Edit the code", code)
        if new_code != code:
            with open(app.path, "w") as f:
                f.write(new_code)
            st.success("code updated")
