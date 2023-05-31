import logging
import environment


# Create a logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

# Create a file handler and set the log file path
log_file = 'mylog.log'
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.getLevelName(environment.FILE_LOGGING_LEVEL)) # type: ignore

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.getLevelName(environment.CONSOLE_LOGGING_LEVEL)) # type: ignore

# Create log formatters
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Set formatters for the handlers
file_handler.setFormatter(file_formatter)
console_handler.setFormatter(console_formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)