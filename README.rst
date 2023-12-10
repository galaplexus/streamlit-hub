Streamlit App Hub
=================

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: LICENSE

Overview
--------

Streamlit App Hub is a Python application that allows you to manage multiple Streamlit apps from a central hub. It provides an interactive web interface where you can add new Streamlit apps, start them, and gracefully exit the application.

Features
--------

- **Manage Multiple Streamlit Apps:** Easily start, stop, and add new Streamlit apps.
- **Interactive Web Interface:** User-friendly interface for app management.
- **Logging:** Configurable logging with colored console output and a log file.

Getting Started
---------------

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/streamlit-app-hub.git
   cd streamlit-app-hub
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit App Hub:

   ```bash
   streamlit run streamlit_manager.py
   ```

4. Access the web interface at `http://localhost:8501` in your browser.

Configuration
-------------

- Streamlit apps are configured in the `streamlit_apps.json` file. Add new app information to this file.

Logging
-------

- Logs are available both in the console with colored output and in the `app.log` file.

Contributing
------------

Contributions are welcome! Please read `CONTRIBUTING.rst` for details on how to contribute to this project.

License
-------

This project is licensed under the MIT License - see the `LICENSE` file for details.