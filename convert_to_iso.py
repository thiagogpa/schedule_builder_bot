from datetime import datetime

def convert_to_iso(date_string, time_string):
    current_year = datetime.now().year
    date_string_with_year = f"{current_year}/{date_string} {time_string}"
    date_obj = datetime.strptime(date_string_with_year, '%Y/%m/%d %I:%M%p')
    iso_date = date_obj.isoformat()
    # print(f"ISO Date: {iso_date}")
    return iso_date

# date_string = "04/23"
# time_string = "08:00AM"
# iso_date = convert_to_iso(date_string, time_string)

