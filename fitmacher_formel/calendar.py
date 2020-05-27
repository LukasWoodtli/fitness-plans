from datetime import datetime

from icalendar import Event, Calendar


class CalendarEvent:
    def __init__(self, summary, date, description=""):
        self.summary = summary
        self.date = date
        self.description = description

    def get_event(self):
        event = Event()
        event.add('summary', self.summary)
        event.add('dtstart', self.date)
        event.add('dtend', self.date)
        event.add('dtstamp', datetime.now())
        event.add('description', self.description)
        return event

    def add_to_cal(self, cal):
        cal.add_component(self.get_event())


def add_to_calender(workout_events):
    cal = Calendar()

    cal.add('prodid', "Fitness")
    cal.add('version', '2.0')
    [event.add_to_cal(cal) for event in workout_events]

    return cal