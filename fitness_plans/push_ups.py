#!/usr/bin/env python3

import collections
import datetime
from datetime import date, time, timedelta
#from bs4 import BeautifulSoup
#from itertools import chain
from fitness_plans.lib.workout_calendar import CalendarEvent, WorkoutCalendar

Workout = collections.namedtuple('Workout', ['sets', 'reps', 'break_in_secs'])

# CURRENT_REPS = [
#     "6_TO_10",
#     "11_TO_20",
#     "21_TO_25",
#     "26_TO_30",
#     "31_TO_40",
#     "40_AND_MORE",
# ]
#
#
# def is_workout_row(i):
#     return i % 2 == 0
#
#
# def parse_workout_row(row):
#     workouts = []
#     for cell in row.find_all('td')[1:]:
#         workout = cell.text.split("+")[0]
#         workout = workout.split("x")
#         workouts.append((int(workout[0]),
#                          int(workout[1]), 0))
#
#     return workouts
#
#
# def parse_break_row(row):
#     breaks = []
#     for cell in row.find_all('td')[1:]:
#         break_ = cell.text.replace('s', '')
#         breaks.append(int(break_.strip()))
#
#     return breaks
#
#
# def main():
#     with open("pushups.html") as fp:
#         soup = BeautifulSoup(fp, 'html.parser')
#         tables = soup.find_all('table')
#         assert len(tables) == 2
#         for i, table in enumerate(tables):
#             print(f"WEEK_{i+1} =")
#             parse_table(table)
#
#
# def parse_table(first_table):
#     rows = first_table.find_all('tr')[1:]
#     weeks = []
#     number_of_rows = len(rows)
#     assert number_of_rows % 2 == 0
#     for i in range(int(number_of_rows / 2)):
#         workouts_for_week = parse_workout_row(rows[i * 2])
#         breaks = parse_break_row(rows[i * 2 + 1])
#         week = []
#         for i, workout in enumerate(workouts_for_week):
#             week.append(Workout(workout[0], workout[1], breaks[i]))
#         weeks.append(week)
#
#     weeks_dict = {}
#     for i, w in enumerate(weeks):
#         reps = CURRENT_REPS[i]
#         weeks_dict[reps] = w
#     print(weeks_dict)


# Generated with the code above form
# https://m.fitforfun.de/workout/krafttraining/liegestuetze-100-stueck-so-schaffen-sies_aid_9794.html
WORKOUT_WEEKS = [
    {
        '6_TO_10': [Workout(sets=4, reps=5, break_in_secs=60), Workout(sets=4, reps=6, break_in_secs=90), Workout(sets=4, reps=8, break_in_secs=120)],
        '11_TO_20': [Workout(sets=4, reps=9, break_in_secs=60), Workout(sets=4, reps=10, break_in_secs=90), Workout(sets=4, reps=12, break_in_secs=120)],
        '21_TO_25': [Workout(sets=4, reps=14, break_in_secs=60), Workout(sets=4, reps=15, break_in_secs=90), Workout(sets=4, reps=17, break_in_secs=120)],
        '26_TO_30': [Workout(sets=4, reps=16, break_in_secs=60), Workout(sets=4, reps=18, break_in_secs=45), Workout(sets=7, reps=15, break_in_secs=45)],
        '31_TO_40': [Workout(sets=4, reps=22, break_in_secs=60), Workout(sets=7, reps=16, break_in_secs=45), Workout(sets=7, reps=18, break_in_secs=45)],
        '40_AND_MORE': [Workout(sets=4, reps=30, break_in_secs=60), Workout(sets=7, reps=20, break_in_secs=45), Workout(sets=7, reps=25, break_in_secs=45)]},
    {
        '6_TO_10': [Workout(sets=4, reps=8, break_in_secs=60), Workout(sets=4, reps=11, break_in_secs=90), Workout(sets=4, reps=11, break_in_secs=120)],
        '11_TO_20': [Workout(sets=4, reps=11, break_in_secs=60), Workout(sets=4, reps=13, break_in_secs=90), Workout(sets=4, reps=15, break_in_secs=120)],
        '21_TO_25': [Workout(sets=4, reps=16, break_in_secs=60), Workout(sets=4, reps=20, break_in_secs=90), Workout(sets=4, reps=23, break_in_secs=120)],
        '26_TO_30': [Workout(sets=4, reps=20, break_in_secs=60), Workout(sets=4, reps=25, break_in_secs=45), Workout(sets=8, reps=18, break_in_secs=45)],
        '31_TO_40': [Workout(sets=4, reps=25, break_in_secs=60), Workout(sets=8, reps=20, break_in_secs=45), Workout(sets=8, reps=22, break_in_secs=45)],
        '40_AND_MORE': [Workout(sets=4, reps=35, break_in_secs=60), Workout(sets=8, reps=28, break_in_secs=45), Workout(sets=8, reps=30, break_in_secs=45)]
    }
]


class PushUps:
    CALENDAR_NAME = "PushUps"

    def __init__(self, start_date=date.today(), workout_time_of_day=time(6, 0, 0)):
        self.workout_start = start_date
        self.workout_time_of_day = workout_time_of_day

    def create_workout_calendar(self):
        output_file_path = f'{self.CALENDAR_NAME}.ics'
        with open(output_file_path, 'w') as f_out:
            workouts_as_ical = self._create_workouts()
            f_out.writelines(workouts_as_ical)

    def _create_workouts(self):
        CURRENT_FITNESS_LEVEL = '11_TO_20'

        all_workouts = []

        workout_date = self._get_monday_of_starting_week()

        for week in WORKOUT_WEEKS:
            workouts = week[CURRENT_FITNESS_LEVEL]
            assert len(workouts) == 3

            ws = self._create_workouts_for_week(workout_date, workouts)
            all_workouts.extend(ws)
            workout_date += timedelta(weeks=1)

        cal = WorkoutCalendar(all_workouts)

        return cal.get_all_as_ical()

    def _create_workouts_for_week(self, first_workout_date, workouts):
        workout_date = first_workout_date
        ws = []
        for workout in workouts:
            text = f"Reps: {workout.reps}\n" \
                   f"Sets: {workout.sets}\n" \
                   "1 set sub-maximal\n" \
                   f"Break: {workout.break_in_secs} s"

            calendar_workout_date = datetime.datetime.combine(date=workout_date, time=self.workout_time_of_day)
            w = CalendarEvent("Push Ups", calendar_workout_date, text, alarm=True)
            ws.append(w)
            workout_date += timedelta(days=2)

        return ws

    def _get_monday_of_starting_week(self):
        monday = self.workout_start - timedelta(days=self.workout_start.weekday())
        assert monday.weekday() == 0
        return monday


if __name__ == '__main__':  # pragma: no cover
    p = PushUps()
    p.create_workout_calendar()
