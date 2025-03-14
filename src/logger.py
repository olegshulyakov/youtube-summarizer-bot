# youtube_summarizer_bot/logger.py
import logging
import sys

def setup_logger(name, log_level=logging.INFO, log_file=None):
    """
    Sets up a logger with the given name, level, and optional file handler.

    Args:
        name (str): The name of the logger (usually __name__).
        log_level (int): The logging level (e.g., logging.DEBUG, logging.INFO).
        log_file (str, optional): The path to a log file. If None, logs only to the console.

    Returns:
        logging.Logger: The configured logger object.
    """

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.handlers = [] # Remove any existing handlers

    # Console handler
    ch = logging.StreamHandler(sys.stdout)  # Use sys.stdout for consistent output
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler (optional)
    if log_file:
        fh = logging.FileHandler(log_file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

# Example usage (you wouldn't typically put this directly *in* the logger module,
# but it shows how to use it):

# Create a logger for the main application
# app_logger = setup_logger("my_app") # This line would typically be in main.py

# Log some messages in main.py or other modules:
# app_logger.debug("This is a debug message.")
# app_logger.info("This is an info message.")
# app_logger.warning("This is a warning message.")
# app_logger.error("This is an error message.")
# app_logger.critical("This is a critical message.")
