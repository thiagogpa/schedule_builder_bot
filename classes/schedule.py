"""
    Represents a schedule for a specific day, including a list of events.

    The `Schedule` class provides a way to manage a schedule for a given day, including
    the ability to add events to the schedule. Each event is represented as a dictionary
    with the following keys:

    - `start_time`: The start time of the event.
    - `end_time`: The end time of the event.
    - `event_type`: The type of the event.
    - `event_name`: The name of the event.
    - `event_id`: The unique identifier for the event.
    """

class Schedule:
    def __init__(self, day, date):
        self.day = day
        self.date = date
        self.events = []

    def add_event(self, start_time, end_time, event_type, event_name, event_id):
        self.events.append({
            'start_time': start_time,
            'end_time': end_time,
            'event_type': event_type,
            'event_name': event_name,
            'event_id': event_id
        })