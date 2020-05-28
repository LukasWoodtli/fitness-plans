from datetime import datetime

from icalendar import Event
from icalendar import Calendar as iCal

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


class Calendar:
    def __init__(self, workouts):
        super().__init__()
        self.cal = iCal()
        self._add_to_calender(workouts)

    def _add_to_calender(self, workout_events):
        self.cal.add('prodid', "Fitness")
        self.cal.add('version', '2.0')
        [event.add_to_cal(self.cal) for event in workout_events]

    def get_all_as_ical(self):
        return self.cal.to_ical().decode('utf-8')