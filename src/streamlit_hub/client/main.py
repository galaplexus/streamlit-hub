import os
import sys

# from streamlit.web import cli as stcli
import logging
import streamlit_hub.client
import runpy

logger = logging.getLogger(__name__)


def main():
    streamlit_script_path = os.path.join(os.path.dirname(streamlit_hub.client.__file__), "app.py")
    sys.argv = ["streamlit", "run", streamlit_script_path, "--theme.base", "dark", "--theme.primaryColor", "orange"]
    runpy.run_module("streamlit", run_name="__main__")


if __name__ == "__main__":
    main()
