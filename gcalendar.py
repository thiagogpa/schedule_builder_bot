"""
Provides functions for interacting with the Google Calendar API.

The `get_calendar_service` function creates a Google Calendar API service client using the provided credentials.

The `create_event` function creates a new event in the user's Google Calendar based on the provided `Schedule` object.

The `create_schedule` function parses a message containing a schedule and creates events in the user's Google Calendar for each event in the schedule.

The `list_events` function retrieves a list of events from the user's Google Calendar within a specified time range.

The `delete_all_events` function deletes all events from the user's Google Calendar within a specified time range.

The `print_calendars` function prints a list of the user's Google Calendars.

The `list_calendars` function retrieves a list of the user's Google Calendars and calls `print_calendars` to display them.

The `create_calendar` function creates a new Google Calendar for the user.
"""
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import Resource
from datetime import datetime, time, timedelta
import os
from googleapiclient import errors
from sys import stdout
from logger import logger
from classes.telegram_user import TelegramUser
from bot_handler import bot
from classes.schedule import Schedule
from convert_to_iso import convert_to_iso


def get_calendar_service(creds) -> Resource:
    service = build("calendar", "v3", credentials=creds)
    return service


def create_event(user: TelegramUser, schedule: Schedule):
    logger.debug(create_event)
    gcalendar_service = get_calendar_service(user.google_credential)

    for event in schedule.events:
        # print(event)
        event_result = (
            gcalendar_service.events()
            .insert(
                calendarId=user.calendar_id,
                body={
                    "summary": event["event_type"],
                    # "description": 'This is a tutorial example of automating google calendar with python',
                    "start": {
                        "dateTime": event["start_time"],
                        "timeZone": "America/Toronto",
                    },
                    "end": {
                        "dateTime": event["end_time"],
                        "timeZone": "America/Toronto",
                    },
                },
            )
            .execute()
        )


def create_schedule(user: TelegramUser, message):
    logger.debug(create_schedule)
    bot.sendMessage(
        user.user_id, "I'm creating the schedule now, give me a moment")
    entries = message.split("\n\n")

    schedules = []

    for entry in entries:
        try:
            splitEntry = entry.split("\n")
            day, date = splitEntry[0].split()
            schedule = Schedule(day=day, date=date)

            for i in range(1, len(splitEntry), 2):
                try:
                    start_time_str, void, end_time_str, event_type_str = splitEntry[
                        i
                    ].split()
                    event_type, event_name, event_id = splitEntry[i + 1].split(
                    )
                except ValueError:
                    logger.debug("Could not parse event")
                    continue

                start_time, end_time = convert_to_iso(
                    date, start_time_str, end_time_str)

                schedule.add_event(
                    start_time=start_time,
                    end_time=end_time,
                    event_type=event_type,
                    event_name=event_name,
                    event_id=event_id,
                )

        except ValueError:
            logger.debug("Could not parse schedule")
            continue

        if len(schedule.events) == 0:
            logger.debug("No events for this schedule")
        else:
            schedules.append(schedule)

    if schedules:
        for schedule in schedules:
            # schedule.print_schedule()
            create_event(user, schedule)
        bot.sendMessage(user.user_id, "Your schedule has been updated")
        logger.info("done adding")
    else:
        logger.debug("Didnt parse any schedules")
        bot.sendMessage(
            user.user_id, "Sorry, I coulnd't create a schedule with what you provided. Make sure you send it on the expected layout. You can use /help to get more info."
        )


def list_events(user: TelegramUser, next_week=None):
    gcalendar_service = get_calendar_service(user.google_credential)

    if next_week:
        start_date = datetime.now().date() + timedelta(days=(datetime.now().weekday()))
    else:
        start_date = datetime.now().date() - timedelta(days=datetime.now().weekday() + 1)

    start_time = datetime.combine(start_date, time.min).isoformat() + "Z"
    end_date = start_date + timedelta(days=6)
    end_time = datetime.combine(end_date, time.max).isoformat() + "Z"

    logger.debug(f"start_time: {start_time} end_time: {end_time}")

    events_result = (
        gcalendar_service.events()
        .list(
            #    calendarId='primary', timeMin=now,
            calendarId=user.calendar_id,
            # timeMin=now,
            timeMin=start_time,
            timeMax=end_time,
            maxResults=100,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
        logger.debug("No events found")
    for event in events:
        return events


def delete_all_events(user: TelegramUser, next_week=None):
    logger.debug("delete_all_events")
    gcalendar_service = get_calendar_service(user.google_credential)
    events = list_events(user, next_week)

    logger.debug(events)

    if events == None:
        bot.sendMessage(user.user_id, "No schedule was found")

    try:
        for event in events:
            try:
                gcalendar_service.events().delete(
                    calendarId=user.calendar_id,
                    eventId=event["id"],
                ).execute()
            except errors.HttpError:
                logger.debug("Failed to delete event")

            logger.debug("Event deleted")

        bot.sendMessage(user.user_id, "This week's schedule has been deleted")
    except:
        pass


def print_calendars(calendar_list, user: TelegramUser):
    # Print the calendars
    for calendar in calendar_list.get("items", []):
        calendar_id = calendar["id"]
        calendar_summary = calendar["summary"]
        # print(f"Calendar ID: {calendar_id}, Summary: {calendar_summary}")
        message = f"Calendar ID: {calendar_id} Summary: {calendar_summary}"

        logger.info(message)
        bot.sendMessage(user.user_id, message)


def list_calendars(user: TelegramUser) -> None:
    logger.debug("list_calendars")

    logger.debug(user.google_credential)

    # Create a service client using the credentials
    # service = build("calendar", "v3", credentials=credentials)
    gcalendar_service = get_calendar_service(user.google_credential)

    # Retrieve a list of calendars
    calendar_list = gcalendar_service.calendarList().list().execute()
    print_calendars(calendar_list, user)


def create_calendar(user: TelegramUser):
    logger.debug("create_calendar")

    # Create a service client using the credentials
    # service = build("calendar", "v3", credentials=credentials)
    gcalendar_service = get_calendar_service(user.google_credential)

    calendar = {
        "summary": "WORK SCHEDULE",
        "timeZone": "UTC",  # Set your desired time zone
    }

    created_calendar = gcalendar_service.calendars().insert(body=calendar).execute()
    user.calendar_id = created_calendar["id"]
    user.save_user()

    logger.debug("New Calendar ID: " + user.calendar_id)

    return True
