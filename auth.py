import json
from flask import Flask, request, redirect
from google.oauth2.credentials import Credentials

from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from logger import logger
import environment

# Store user credentials in a dictionary
user_credentials = {}


def credentials_to_dict(credentials):
    return {
        "google_credential": {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes,
        }
    }


def load_all_user_credentials():
    logger.debug("load_all_user_credentials")
    try:
        with open(environment.CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# Save user credentials to the JSON file
def save_user_credentials(user_credentials):
    logger.debug("save_user_credentials")
    with open(environment.CREDENTIALS_FILE, "w") as file:
        json.dump(user_credentials, file, indent=4)


def authorize_user(user_id):
    logger.debug("authorize_user")
    # Create a flow instance with the client ID, client secret, and redirect URI
    flow = Flow.from_client_secrets_file(
        environment.CLIENT_SECRET_FILE,
        scopes=environment.SCOPE,
        redirect_uri=environment.REDIRECT_URI,
    )

    # Set the access type to 'offline' to request refresh tokens
    flow.access_type = "offline"

    # Set the prompt to 'consent' to ensure offline access is requested
    flow.prompt = "consent"

    # Generate the authorization URL with a unique state parameter
    authorization_url, state = flow.authorization_url(state=user_id)

    # # Store the state parameter in the user_credentials dictionary
    user_credentials[user_id] = {}

    # Redirect the user to the authorization URL
    return authorization_url
    # return redirect(authorization_url)


def validate_userid():
    logger.debug("validate_userid")
    # Retrieve the authorization code and state parameter from the callback request
    authorization_code = request.args.get("code")
    state = request.args.get("state")

    user = TelegramUser()
    user.user_id = state

    # Create a flow instance using the stored client secrets
    flow = Flow.from_client_secrets_file(
        environment.CLIENT_SECRET_FILE,
        scopes=environment.SCOPE,
        redirect_uri=environment.REDIRECT_URI,
    )

    # Exchange the authorization code for credentials
    flow.fetch_token(authorization_response=request.url)

    user.google_credential = flow.credentials    
    user.save_user()

    # Redirect the user to a success page or perform further actions
    return user
    # return credentials


from  classes.telegram_user import TelegramUser