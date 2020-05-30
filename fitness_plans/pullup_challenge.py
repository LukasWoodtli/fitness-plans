#!/usr/bin/env python3
from datetime import timedelta, date, datetime
import requests
from bs4 import BeautifulSoup

from fitness_plans.workout_calendar import CalendarEvent, WorkoutCalendar


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


class PullUpChallenge:

    def __init__(self, week_no=1, start_date=date.today(), workout_frequecy=timedelta(days=2)):
        self._week_no = 1
        self.workout_start = start_date
        self.workout_frequency = workout_frequecy

    def _get_all_workouts(self):
        table_body = self._fetch_page_and_parse_table()

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
                workout_day = Workout(self._week_no, title, subtitle)
                all_workouts.append(workout_day)

            else:
                assert workout_day
                cols = [ele.text.strip() for ele in cols]
                assert len(cols) == 3
                workout_day.append_workout_step(*cols)

        return all_workouts

    def _fetch_page_and_parse_table(self):
        page = self._fetch_page()
        return self._parse_table(page)

    def _fetch_page(self):
        request = requests.get('https://twentypullups.com/')
        soup = BeautifulSoup(request.text, 'html.parser')
        return soup

    def _parse_table(self, html_soup):
        week_no_text = f"Week {self._week_no}"
        # link to week
        weeks = [i.get('href') for i in html_soup.find_all('a') if week_no_text in i.text]

        # parse table
        week_page_request = requests.get(weeks[0])
        week_page = BeautifulSoup(week_page_request.text, 'html.parser')

        table = week_page.find('table')
        table_body = table.find('tbody')

        return table_body

    def _workouts_to_cal_events(self):
        workouts = self._get_all_workouts()
        cal_events = []
        workout_date = self.workout_start
        for workout in workouts:
            title = workout.get_full_title()
            description = workout.get_description_text()
            event = CalendarEvent(title, workout_date, description)
            workout_date = workout_date + self.workout_frequency
            cal_events.append(event)
        return cal_events

    def _create_workouts_from_text(self):
        events = self._workouts_to_cal_events()
        cal = WorkoutCalendar(events)
        return cal.get_all_as_ical()

    def create_workout_calendar(self):
        cal_text = self._create_workouts_from_text()
        with open("pullup.ics", 'w') as out_file:
            out_file.writelines(cal_text)


if __name__ == "__main__":
    challenge = PullUpChallenge()
    challenge.create_workout_calendar()