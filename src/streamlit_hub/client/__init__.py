import logging
from logging.handlers import RotatingFileHandler
from colorlog import ColoredFormatter


def configure_logging(log_file="app.log", log_level=logging.INFO):
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Create a file handler and set the log level
    file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=2)
    file_handler.setLevel(log_level)

    # Create a formatter for the file handler (without colors)
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)

    # Create a colored formatter for the console
    console_formatter = ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s %(white)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            "DEBUG": "blue",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red",
        },
    )

    # Set the formatter for the console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


configure_logging()
