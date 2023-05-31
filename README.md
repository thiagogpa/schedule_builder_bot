[![Docker Build](https://github.com/thiagogpa/schedule_builder_bot/actions/workflows/docker-build.yml/badge.svg?branch=main)](https://github.com/thiagogpa/schedule_builder_bot/actions/workflows/docker-build.yml)


# Work Schedule Bot

Welcome to our Work Schedule Bot! This bot helps you manage your work schedules seamlessly using Google Calendar integration. Create, update, and delete work schedules effortlessly, ensuring efficient coordination with your team. Stay organized and stay on top of your work schedule with our Work Schedule Bot powered by Google Calendar!

## Getting Started

To start using the Work Schedule Bot, follow these steps:

1. Begin a conversation with the bot by typing `/start`.
2. The bot will require access to your Google Calendar. This is necessary for setting up and managing your work schedule. Rest assured, the bot will create a new calendar, ensuring that any updates are reflected in that calendar only. You can even share that calendar with your family members so they can be aware of your working hours.
3. When granting access to your calendar, you might see a warning screen from Google. This is a temporary message and is displayed while Google verifies the authenticity of the bot.

## Updating Your Schedule

To add a new schedule, use the `/update_schedule` command and provide the schedule in the following format:

    Sunday/Dimanche/Domingo, 05/23
    08:00AM - 11:00AM  WRK
    CE_LEADER, 09999, 09999_LEADERSHIP
    11:00AM - 01:00PM  WRK
    LOD, 09999, 09999_LEADERSHIP
    01:00PM - 03:00PM  WRK
    CE_LEADER, 09999, 09999_KBM
    03:00PM - 05:00PM  WRK
    LOD, 09999, 09999_LEADERSHIP


## Updating and Deleting Schedules

If you need to make changes to your schedule, the best way to do so is by using the `/delete_week_schedule` or `/delete_next_week_schedule` command. Afterward, you can send the updated schedule using the `/update_schedule` command.

## Recreating a Deleted Calendar

In the event that you accidentally delete the Google calendar created by the bot, you can create a new one by using the `/create_calendar` command. Please note that the bot cannot automatically detect if the calendar was deleted.

## Additional Commands

- `/list_calendars`: View a list of all your calendars.
- `/create_calendar`: Create a new calendar. Only use this command if you mistakenly deleted your calendar.
- `/delete_week_schedule`: Erase all events for the current week.
- `/delete_next_week_schedule`: Remove all events for the upcoming week.

Enjoy using our Work Schedule Bot and make the most of efficient work schedule management with Google Calendar integration!
