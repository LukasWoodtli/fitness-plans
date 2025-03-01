#!/usr/bin/env python3
""""Taken from: https://twentypullups.com/"""
from datetime import timedelta, date
from pathlib import Path

import pymupdf

from fitness_plans.lib.workout_calendar import CalendarEvent, WorkoutCalendar


class Workout:
    def __init__(self, day, week, subtitle, sets_descriptions, sets):
        self.day = day
        self.week = week
        self.subtitle = subtitle
        self.sets_descriptions = sets_descriptions
        self.easy_set = []
        self.medium_set = []
        self.hard_set = []
        for set in sets:
            easy_set, medium_set, hard_set = set[1:]
            self.easy_set.append(easy_set)
            self.medium_set.append(medium_set)
            self.hard_set.append(hard_set)

    def get_full_title(self):
        return f"Day {self.day} (Week {self.week})"

    def _get_workout_set_text(self, level):
        text = f"{level.title()}:\n"

        if level.lower() == "easy":
            workout_set = self.easy_set
            index = 0
        elif level.lower() == "medium":
            workout_set = self.medium_set
            index = 1
        elif level.lower() == "hard":
            workout_set = self.hard_set
            index = 2
        else:
            raise Exception(f"Level not known: {level}")

        prerequisites = self.sets_descriptions[index]

        text += f"Prerequisites: {prerequisites}\n\n"

        for i, s in enumerate(workout_set, 1):
            text += f"\tSet {i}: {s}\n"
        text += "\n\n"

        return text

    def get_description_text(self):
        text = f"{self.subtitle}\n\n"
        text += self._get_workout_set_text("Easy")
        return text


class PullUpChallenge:

    def __init__(self, week_no=1, start_date=date.today(), workout_frequency=timedelta(days=2)):
        self._week_no = week_no
        self.workout_start = start_date
        self.workout_frequency = workout_frequency
        # PDF from: https://twentypullups.com/20-pull-ups_ilka-helo.pdf
        self.pdf = Path(__file__).parent / "pullup_challenge" / "20-pull-ups_ilka-helo.pdf"

    def _get_all_workouts(self):
        return self._read_pdf_and_parse_tables()

    def _read_pdf_and_parse_tables(self):
        pages = self._read_pdf()
        return self._parse_tables(pages)

    def _read_pdf(self):
        with pymupdf.open(self.pdf) as doc:
            for page in doc.pages():
                text = page.get_text()
                text = text.replace('© 2008 Olli Sikstus, Inspired by the Hundred Push Ups', '')
                yield text

    def _parse_tables(self, pdf_pages):
        week_no_text = f"Week {self._week_no}"
        # link to week
        week = [w for w in pdf_pages if w.startswith(week_no_text)]
        assert len(week) == 1
        week = week[0]

        days = week.split("Day")
        week_no = days[0].split("\n")[0].replace("Week", "").strip()
        week_no = int(week_no)
        days = days[1:]
        for day in days:
            sets = day.split("\n")
            sets = [s.strip() for s in sets if s.strip() != ""]
            day_no = int(sets[0])
            rest_description = sets[1]
            sets_descriptions = sets[2:5]
            sets = sets[5:]
            entries_per_set = 4
            sets = [sets[i:i + entries_per_set] for i in range(0, len(sets), entries_per_set)]
            yield Workout(day_no, week_no, rest_description, sets_descriptions, sets)

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