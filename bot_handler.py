from logger import logger
from flask import Flask, request, redirect
from google_auth_oauthlib.flow import Flow
import telepot
from telepot.loop import MessageLoop
from auth import authorize_user
import environment

global bot
bot = telepot.Bot(environment.TELEGRAM_TOKEN)

# Start authentication process
def handle_start(chat_id):
    logger.debug("handle_start")

    # Create a flow instance with the client ID, client secret, and redirect URI
    flow = Flow.from_client_secrets_file(
        environment.CLIENT_SECRET_FILE,
        scopes=environment.SCOPE,
        redirect_uri=environment.REDIRECT_URI,
    )

    auth_url, _ = flow.authorization_url(prompt="consent")
    bot.sendMessage(
        chat_id,
        text="Please click the link below to authenticate with Google:\n{}".format(
            authorize_user(chat_id)
        ),
    )

def donate_command(chat_id):
    donate_link = "https://www.buymeacoffee.com/thiagogpa"
    message = "Thank you for considering a donation! You can donate using the following link:\n{}".format(donate_link)
    bot.sendMessage(chat_id, message)


def help_command(chat_id):
    help_message = '''<b>Welcome to our Work Schedule Bot!</b>
This bot helps you manage your work schedules seamlessly using Google Calendar integration. Create, and delete work schedules effortlessly, ensuring efficient coordination with your team. Simply send your schedule in the expected layout, and the bot will handle the rest. Stay organized and stay on top of your work schedule with our Work Schedule Bot powered by Google Calendar!

Once you <b>/start</b> a conversation with the bot, you'll need to provide it access to your Google Calendar so it can set up your schedule for you. Don't worry, it will create a new calendar, so any updates will be reflected in that one only. You can even share that calendar with your family members so they can know when you are working. Please note that you may see a temporary warning screen from Google while granting access to your calendar as they verify this bot's authenticity.

To add a new schedule, use the command <b>/update_schedule</b> and provide your schedule in the following layout:

Sunday/Dimanche/Domingo, 05/23
08:00AM - 11:00AM  WRK
CE_LEADER, 09999, 09999_LEADERSHIP
11:00AM - 01:00PM  WRK
LOD, 09999, 09999_LEADERSHIP
01:00PM - 03:00PM  WRK
CE_LEADER, 09999, 09999_KBM
03:00PM - 05:00PM  WRK
LOD, 09999, 09999_LEADERSHIP

Monday/Lundi/Lunes, 05/24
01:00PM - 03:00PM  WRK
CE_LEADER, 09999, 09999_KBM
03:00PM - 05:00PM  WRK
LOD, 09999, 09999_LEADERSHIP
05:00PM - 07:00PM  WRK
CE_LEADER, 09999, 09999_KBM
07:00PM - 09:00PM  WRK
LOD, 09999, 09999_LEADERSHIP
09:00PM - 10:00PM  WRK
CE_LEADER, 09999, 09999_LEADERSHIP

If you want to make changes to your calendar and update it, the best way is to use the options <b>/delete_week_schedule</b> or <b>/delete_next_week_schedule</b> to remove all events and then send the updated schedule using <b>/update_schedule</b>.

If you accidentally deleted the Google calendar created by the bot, you'll need to create a new one using <b>/create_calendar</b> since the bot cannot detect if the calendar was deleted.

Available commands:
<b>/list_calendars</b> - View a list of all your calendars
<b>/create_calendar</b> - Create a new calendar (use this if you deleted your calendar by mistake)
<b>/delete_week_schedule</b> - Erase all events for the current week
<b>/delete_next_week_schedule</b> - Remove all events for the upcoming week

If you like this bot and would like to support me you can donate at
https://www.buymeacoffee.com/thiagogpa

Or if you just want to know who is the developer you find me at
https://thiago.cloud/
'''

    bot.sendMessage(chat_id, help_message, parse_mode='HTML')
