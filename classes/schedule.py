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