"""
Converts a date string and start/end time strings to ISO format datetime strings.

Args:
    date_string (str): A string representing the date in the format 'mm/dd'.
    start_time_string (str): A string representing the start time in the format 'hh:mmAM/PM'.
    end_time_string (str): A string representing the end time in the format 'hh:mmAM/PM'.

Returns:
    Tuple[str, str]: A tuple containing the ISO format start datetime string and end datetime string.
"""
from datetime import datetime, timedelta


def convert_to_iso(date_string, start_time_string, end_time_string):
    current_year = datetime.now().year
    date_string_with_year = f"{current_year}/{date_string}"
    date_obj = datetime.strptime(date_string_with_year, '%Y/%m/%d').date()

    start_time_obj = datetime.strptime(start_time_string, '%I:%M%p').time()
    end_time_obj = datetime.strptime(end_time_string, '%I:%M%p').time()

    start_datetime = datetime.combine(date_obj, start_time_obj)
    end_datetime = datetime.combine(date_obj, end_time_obj)

    if end_datetime < start_datetime:
        end_datetime += timedelta(days=1)

    start_iso = start_datetime.isoformat()
    end_iso = end_datetime.isoformat()

    return start_iso, end_iso

# date_string = "04/23"
# time_string = "08:00AM"
# iso_date = convert_to_iso(date_string, time_string)
