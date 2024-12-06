import logging
import os
import environment

# Define the log file path and create the logs directory if it doesn't exist
log_file = 'logs/app.log'
os.makedirs(os.path.dirname(log_file), exist_ok=True)

# Ensure 'mylog.log' is not a directory
if os.path.exists(log_file) and os.path.isdir(log_file):
    raise IsADirectoryError(f"'{log_file}' exists as a directory. Remove or rename it.")

# Create a logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

# Create a file handler and set the log file path
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.getLevelName(environment.FILE_LOGGING_LEVEL))  # type: ignore

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.getLevelName(environment.CONSOLE_LOGGING_LEVEL))  # type: ignore

# Create log formatters
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Set formatters for the handlers
file_handler.setFormatter(file_formatter)
console_handler.setFormatter(console_formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Example log message
logger.info("Logger initialized and ready!")
