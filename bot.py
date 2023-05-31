from logger import logger
import telepot
from telepot.loop import MessageLoop

from flask import Flask, request, redirect
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from bot_handler import handle_start, bot, help_command, donate_command
import os
import environment
from classes.telegram_user import TelegramUser
from auth import authorize_user, validate_userid
from gcalendar import (
    create_calendar,
    list_calendars,
    list_events,
    create_schedule,
    delete_all_events,
)
from backup import start_backup_thread


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

previous_messages = {}

# Create a Flask web application
app = Flask(__name__)

# Create a flow instance with the client ID, client secret, and redirect URI
flow = Flow.from_client_secrets_file(
    environment.CLIENT_SECRET_FILE,
    scopes=environment.SCOPE,
    redirect_uri=environment.REDIRECT_URI,
)


def load_user(chat_id) -> TelegramUser:
    user = TelegramUser()
    user.load_user(chat_id)
    return user


# Route for initiating the OAuth flow
@app.route("/authorize/<user_id>")
def authorize(user_id):
    logger.debug("authorize")
    return authorize_user(user_id)


# Route for handling the OAuth callback
@app.route("/oauth2callback")
def callback():
    logger.debug("callback")
    user = validate_userid()
    if user.google_credential:
        bot.sendMessage(
            user.user_id,
            text="You're validated successfully, I'll create a new calendar now",
        )
        if create_calendar(user):
            bot.sendMessage(user.user_id, text="Your calendar has been created")
        return "Validated"
    else:
        bot.sendMessage(
            user.user_id, text="Something went wrong, I was not able to validate you"
        )
        return "Valitation unsucessful"


# Route for accessing user's data
@app.route("/user_data/<user_id>")
def user_data(user_id):
    logger.debug("/user_data/<user_id>")
    user = load_user(user_id)

    list_calendars(user)

    return "success"


# Handle incoming messages from Telegram
def handle_message(msg):
    logger.debug("handle_message")
    content_type, chat_type, chat_id = telepot.glance(msg)  # type: ignore

    if content_type == "text":
        command = msg["text"]
        # logger.info("User sent message: {}".format(command))
        logger.info(f"User {chat_id} sent message: {command}")

        user = load_user(chat_id)
        logger.debug(user.google_credential)
        if user:
            logger.debug("logged in")
        else:
            logger.debug("Not logged in")

        # Log user interactions

        logger.debug(f"previous_message = {previous_messages}")

        # Check if the chat_id exists in the dictionary
        if chat_id in previous_messages:
            previous_message = previous_messages[chat_id]
        else:
            previous_message = None

        logger.debug(f"previous_message = {previous_message}")

        # Handle user commands or actions
        if command == "/start":
            if user:
                bot.sendMessage(chat_id, text="Hey you are already logged in")
            else:
                handle_start(chat_id)

        elif command == "/list_events":  # sends message#
            bot.sendMessage(chat_id, "Listing events")
            events = list_events(user)
            try:
                if events:
                    for event in events:  # type: ignore
                        logger.debug(event["summary"])
                        logger.debug(event)
                        bot.sendMessage(chat_id, f"{event['summary']}")
                    bot.sendMessage(chat_id, "This are all the events")
                else:
                    bot.sendMessage(chat_id, "No events found")
            except:
                pass

        elif command == "/create_calendar":
            # Load existing user credentials from the JSON file
            # user_credentials = load_user_credentials(chat_id)
            logger.debug(chat_id)
            if create_calendar(user):
                bot.sendMessage(chat_id, text="Your calendar has been created")

        elif command == "/list_calendars":
            list_calendars(user)

        elif command == "/update_schedule":
            bot.sendMessage(chat_id, text="Send me your schedule in the next message")

        elif command == "/delete_week_schedule":
            bot.sendMessage(chat_id, "Deleting this week's schedule, give me a moment")
            delete_all_events(user)

        elif command == "/delete_next_week_schedule":
            bot.sendMessage(chat_id, "Deleting next week's schedule, give me a moment")
            delete_all_events(user, True)

        elif command == "/donate":  # sends message#
            donate_command(chat_id)
            
        elif command == "/help":  # sends message#
            help_command(chat_id)
        else:
            if previous_message and previous_message["text"] == "/update_schedule":
                create_schedule(user, command)

        # Update the previous message for the chat_id
        previous_messages[chat_id] = msg
        logger.debug(f"msg = {msg}")
        logger.debug(f"previous_message = {previous_messages}")

start_backup_thread(environment.CREDENTIALS_FILE, "bkp")

MessageLoop(bot, handle_message).run_as_thread()
logger.info("Bot started.")


# Run the Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5677)
