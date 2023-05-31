import os
from dotenv import dotenv_values

DEFAULT_CLIENT_SECRET_FILE = "client_secret.json"

DEFAULT_CREDENTIALS_FILE = "user_credentials.json"
DEFAULT_REDIRECT_URI = "http://localhost/oauth2callback"
DEFAULT_FILE_LOGGING_LEVEL = "INFO"
DEFAULT_CONSOLE_LOGGING_LEVEL = "INFO"

# Try loading environment variables from Docker Compose
try:
    # Access the environment variables
    CLIENT_SECRET_FILE = os.environ.get("CLIENT_SECRET_FILE", DEFAULT_CLIENT_SECRET_FILE)
    CREDENTIALS_FILE = os.environ.get("CREDENTIALS_FILE", DEFAULT_CREDENTIALS_FILE)
    REDIRECT_URI = os.environ.get("REDIRECT_URI", DEFAULT_REDIRECT_URI)
    TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
    FILE_LOGGING_LEVEL = os.environ.get("FILE_LOGGING_LEVEL",DEFAULT_FILE_LOGGING_LEVEL)
    CONSOLE_LOGGING_LEVEL = os.environ.get("CONSOLE_LOGGING_LEVEL",DEFAULT_CONSOLE_LOGGING_LEVEL)
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

# SCOPE = [
#     "https://www.googleapis.com/auth/calendar",
#     "https://www.googleapis.com/auth/userinfo.profile",
# ]

SCOPE = [
    "https://www.googleapis.com/auth/calendar"
]
