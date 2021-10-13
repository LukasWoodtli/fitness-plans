from datetime import datetime, timedelta

from icalendar import Event
from icalendar import Calendar
from icalendar import Alarm


class CalendarEvent:
    def __init__(self, summary, date, description="", alarm=False):
        self.summary = summary
        self.date = date
        self.description = description
        self.alarm = alarm

    def get_event_as_ical(self):
        event = Event()
        event.add('summary', self.summary)
        event.add('dtstart', self.date)
        event.add('dtend', self.date)
        event.add('dtstamp', datetime.now())
        event.add('description', self.description)

        if self.alarm:
            alarm = Alarm()
            alarm.add('action', 'DISPLAY')
            alert_time = timedelta(minutes=-15)
            alarm.add('trigger', alert_time)
            event.add_component(alarm)

        return event


class WorkoutCalendar:
    def __init__(self, workouts):
        super().__init__()
        self.cal = Calendar()
        self._add_to_calender(workouts)

    def _add_to_calender(self, workout_events):
        self.cal.add('prodid', "Fitness")
        self.cal.add('version', '2.0')
        for event in workout_events:
            self.cal.add_component(event.get_event_as_ical())

    def get_all_as_ical(self):
        return self.cal.to_ical().decode('utf-8')