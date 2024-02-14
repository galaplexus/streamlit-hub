import streamlit as st
from streamlit_hub.manager.manager import Manager


def toggle_nginx_enabled(manager: Manager):
    manager.nginx_access.toggle_enabled_flag()


def show_config(manager: Manager):
    st.header("Config")

    nginx_path = st.text_input("Nginx config path:", manager.nginx_access.get_config_path())
    if nginx_path:
        manager.nginx_access.set_config_path(nginx_path)

    serving_port = st.number_input("Serving Port:", manager.nginx_access.get_serving_port(), step=1)
    if serving_port:
        manager.nginx_access.set_serving_port(serving_port)

    enabled = st.checkbox(
        "Enabled Flag", manager.nginx_access.get_enabled_flag(), on_change=toggle_nginx_enabled, args=(manager,)
    )

    if enabled and not nginx_path:
        st.warning("Please specify a path for the nginx config file")
