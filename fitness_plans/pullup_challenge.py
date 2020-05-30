#!/usr/bin/env python3
from datetime import timedelta, date, datetime
from icalendar import Calendar, Event
import requests
from bs4 import BeautifulSoup

from fitness_plans.workout_calendar import CalendarEvent, WorkoutCalendar

r = requests.get('https://twentypullups.com/')
soup = BeautifulSoup(r.text, 'html.parser')

WEEK_NO = 1
WEEK_NO_TEXT = f"Week {WEEK_NO}"

# link to week
weeks = [i.get('href') for i in soup.find_all('a') if WEEK_NO_TEXT in i.text]

# parse table
week_page_request = requests.get(weeks[0])
week_page = BeautifulSoup(week_page_request.text, 'html.parser')

table = week_page.find('table')
table_body = table.find('tbody')

class Workout:
    def __init__(self, week, title, subtitle):
        self.week = week
        self.title = title
        self.subtitle = subtitle
        self.easy_set = []
        self.medium_set = []
        self.hard_set = []

    def get_full_title(self):
        return f"{self.title} (Week {self.week})"

    def _get_workout_set_text(self, level):
        text = f"{level.title()}:\n"

        if level.lower() == "easy":
            workout_set = self.easy_set
        elif level.lower() == "medium":
            workout_set = self.medium_set
        elif level.lower() == "hard":
            workout_set = self.hard_set
        else:
            raise Exception(f"Level not known: {level}")

        prerequisites = workout_set[0]
        text += f"Prerequisites: {prerequisites}\n\n"

        for i, s in enumerate(workout_set[1:], 1):
            text += f"\tSet {i}: {s}\n"
        text += "\n\n"

        return text

    def get_description_text(self):
        text = f"{self.subtitle}\n\n"
        text += self._get_workout_set_text("Easy")
        #text += self._get_workout_set_text("Medium")
        #text += self._get_workout_set_text("Hard")
        return text


    def __repr__(self):
        text = self.get_full_title() + "\n"
        text += self.get_description_text() + "\n"

        return text

    def append_workout_step(self, easy_workout, medium_workout, hard_workout):
        self.easy_set.append(easy_workout)
        self.medium_set.append(medium_workout)
        self.hard_set.append(hard_workout)


rows = table_body.find_all('tr')
all_workouts = []
for row in rows:
    cols = row.find_all('td')
    if not cols:
        text = row.text
        text = text.splitlines()
        text = [line.strip() for line in text if line.strip()]
        assert len(text) == 2
        title = text[0]
        assert title.startswith("Day")
        subtitle = text[1]
        assert subtitle.startswith("Rest")
        workout_day = Workout(WEEK_NO, title, subtitle)
        all_workouts.append(workout_day)

    else:
        assert workout_day
        cols = [ele.text.strip() for ele in cols]
        assert len(cols) == 3
        workout_day.append_workout_step(*cols)


WORKOUT_START = date.today()  #+ timedelta(days=2) #date(year=2019, month=10, day=1)
WORKOUT_FREQUENCY = timedelta(days=2)


def workouts_to_cal_events(workouts):
    cal_events = []
    workout_date = WORKOUT_START
    for workout in workouts:
        title = workout.get_full_title()
        description = workout.get_description_text()
        event = CalendarEvent(title, workout_date, description)
        workout_date = workout_date + WORKOUT_FREQUENCY
        cal_events.append(event)
    return cal_events


all_workouts = workouts_to_cal_events(all_workouts)


def add_to_calender(workout_events):
    cal = WorkoutCalendar(workout_events)

    return cal

calendar = add_to_calender(all_workouts)

calendar = calendar.get_all_as_ical()


def get_calendar_as_string():
    return calendar

with open('../test/pullups.ics', 'w') as fout:
    fout.writelines(calendar)
    fout.close()