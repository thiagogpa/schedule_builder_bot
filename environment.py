import os
from dotenv import dotenv_values

DEFAULT_CLIENT_SECRET_FILE = "client_secret.json"

DEFAULT_CREDENTIALS_FILE = "user_credentials.json"
DEFAULT_REDIRECT_URI = "http://localhost/oauth2callback"
DEFAULT_FILE_LOGGING_LEVEL = "INFO"
DEFAULT_CONSOLE_LOGGING_LEVEL = "INFO"
DEFAULT_BACKUP_FREQUENCY = "86400"
DEFAULT_BACKUP_QUANTITY = "30"

# Try loading environment variables from Docker Compose
try:
    # Access the environment variables
    CLIENT_SECRET_FILE = os.environ.get("CLIENT_SECRET_FILE", DEFAULT_CLIENT_SECRET_FILE)
    CREDENTIALS_FILE = os.environ.get("CREDENTIALS_FILE", DEFAULT_CREDENTIALS_FILE)
    REDIRECT_URI = os.environ.get("REDIRECT_URI", DEFAULT_REDIRECT_URI)
    TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
    FILE_LOGGING_LEVEL = os.environ.get("FILE_LOGGING_LEVEL",DEFAULT_FILE_LOGGING_LEVEL)
    CONSOLE_LOGGING_LEVEL = os.environ.get("CONSOLE_LOGGING_LEVEL",DEFAULT_CONSOLE_LOGGING_LEVEL)
    BACKUP_FREQUENCY = os.environ.get("BACKUP_FREQUENCY",DEFAULT_BACKUP_FREQUENCY)
    BACKUP_QUANTITY = os.environ.get("BACKUP_QUANTITY",DEFAULT_BACKUP_QUANTITY)
except KeyError:
    # Load environment variables from .env file
    env_vars = dotenv_values(".env")

    # Access the environment variables
    CLIENT_SECRET_FILE = env_vars.get("CLIENT_SECRET_FILE",DEFAULT_CLIENT_SECRET_FILE)
    CREDENTIALS_FILE = env_vars.get("CREDENTIALS_FILE",DEFAULT_CREDENTIALS_FILE)
    REDIRECT_URI = env_vars.get("REDIRECT_URI",DEFAULT_REDIRECT_URI)
    TELEGRAM_TOKEN = env_vars["TELEGRAM_TOKEN"]
    FILE_LOGGING_LEVEL = env_vars.get("FILE_LOGGING_LEVEL",DEFAULT_FILE_LOGGING_LEVEL)
    CONSOLE_LOGGING_LEVEL = env_vars.get("CONSOLE_LOGGING_LEVEL",DEFAULT_CONSOLE_LOGGING_LEVEL)
    BACKUP_FREQUENCY = env_vars.get("BACKUP_FREQUENCY",DEFAULT_BACKUP_FREQUENCY)
    BACKUP_QUANTITY = env_vars.get("BACKUP_QUANTITY",DEFAULT_BACKUP_QUANTITY)

# SCOPE = [
#     "https://www.googleapis.com/auth/calendar",
#     "https://www.googleapis.com/auth/userinfo.profile",
# ]

SCOPE = [
    "https://www.googleapis.com/auth/calendar"
]
