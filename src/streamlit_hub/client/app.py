import streamlit as st
import importlib
from streamlit_hub.client import config, register, status
import streamlit_hub.manager.manager
from streamlit_hub.manager.manager import Manager

importlib.reload(streamlit_hub.manager.manager)

st.set_page_config(page_title="Streamlit Hub", page_icon="👋", layout="wide")

# Custom CSS styles
custom_styles = """
<style>
</style>
"""

# Inject custom styles
st.markdown(custom_styles, unsafe_allow_html=True)


@st.cache_resource()
def get_manager():
    return Manager()


def run():
    manager = get_manager()
    st.title("App Manager Control Panel")
    page = st.sidebar.radio("Select Page", ["Home", "Register App", "Config"])
    if page == "Home":
        status.show_status(manager)
    elif page == "Register App":
        register.show_register(manager)
    else:
        config.show_config(manager)

    st.markdown(
        """
    **For more information:**
    - [Streamlit Documentation](https://docs.streamlit.io/)
    - [GitHub Repository](https://github.com/galaplexus/streamlit-hub)
    """
    )


if __name__ == "__main__":
    run()
