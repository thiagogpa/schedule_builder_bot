import json
from google.oauth2.credentials import Credentials
from classes.google_credential import refresh_credentials
from logger import logger
from auth import save_user_credentials, load_all_user_credentials
import environment

class TelegramUser:
    def __init__(self):
        self.user_id = None
        self.google_credential = None
        self.calendar_id = None
        self.username = None
        self.first_name = None
        self.last_name = None

    def __bool__(self):
        return bool(self.google_credential)

    def load_user(self, user_id=None,username=None,first_name=None,last_name=None):
        logger.debug("load_user")
        # Load existing user credentials from the JSON file
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

        users_json = load_all_user_credentials()

        # Retrieve the user's credentials from the user_credentials dictionary
        user_dict = users_json.get(str(self.user_id))

        if user_dict:
            logger.debug("user_dict")
            self.json_to_user(user_dict)
            logger.debug(self.google_credential)
            try: 
                logger.debug(self.google_credential.refresh_token) 
            except:
                pass

            if self.google_credential:
                if self.google_credential.refresh_token != None:
                    logger.debug("Updating credentials")
                    # Update the user's credentials in the user_credentials dictionary
                    users_json[str(self.user_id)] = self.user_to_json()
                    save_user_credentials(users_json)
            else:
                logger.debug("Unable to refresh credentials")

            return True
        else:
            return "User not authenticated."
        
    def save_user(self):
        logger.debug("save_user")
        users_json = load_all_user_credentials()
        users_json[str(self.user_id)] = self.user_to_json()
        save_user_credentials(users_json)
        logger.debug("User saved")


        

    def json_to_user(self, user_dict):
        logger.debug("json_to_user")

        logger.debug(self.user_id)
        logger.debug(user_dict)

        # Convert the credentials dictionary to Credentials object
        google_credential = Credentials.from_authorized_user_info(
            user_dict.get("google_credential")
        )
        
        self.calendar_id = user_dict.get("calendar_id")

        self.google_credential = refresh_credentials(google_credential)

    def user_to_json(self):
        logger.debug("user_to_json")
        return {
            "google_credential": {
                "token": self.google_credential.token,
                "refresh_token": self.google_credential.refresh_token,
                "token_uri": self.google_credential.token_uri,
                "client_id": self.google_credential.client_id,
                "client_secret": self.google_credential.client_secret,
                "scopes": self.google_credential.scopes,
            },
            "calendar_id": self.calendar_id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }
