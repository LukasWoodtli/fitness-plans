#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import date, timedelta
import re
import os

from fitmacher_formel.workout_calendar import CalendarEvent, Calendar

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../dfmf.txt')

WORKOUT_START = date.today() + timedelta(days=1) #date(year=2019, month=10, day=1)
FIRST_WORKOUT = 1

BEGIN_TEXT = "GAT .1"  # just a bit obfuscated
BEGIN_TEXT = BEGIN_TEXT[::-1]

END_TEXT = "RIM TIM MUART NENIEM EBEL"  # just a bit obfuscated
END_TEXT = END_TEXT[::-1]

SPLIT_DAY_RE = re.compile(r"([0-9]{1,2}\. TAG[^\n]*)", flags=re.M)


def read_input_file():
    with open(INPUT_FILE, 'r', encoding='utf-8') as infile:
        data = infile.read()
        data = data[data.find(BEGIN_TEXT):]  # remove begin
        data = data.split(END_TEXT)[0]  # remove end
        return data


def split_workouts(data):
    workout_date = WORKOUT_START
    all_workouts = []
    sections = re.split(SPLIT_DAY_RE, data)
    sections = sections[1:]  # first entry is empty
    assert len(sections) % 2 == 0
    for s in range(0, int(len(sections)/2)):
        title = sections[s*2]
        description = title + sections[s * 2 + 1]
        description = re.sub("\n\n+", "\n\n", description)
        event = CalendarEvent(title, workout_date, description)
        all_workouts.append(event)
        workout_date = workout_date + timedelta(days=1)
    return all_workouts



def main():
    fout = open('fitness.ics', 'w')
    workouts_as_ical = create_workuts_from_text()
    fout.writelines(workouts_as_ical)
    fout.close()


def create_workuts_from_text():
    workouts = split_workouts(read_input_file())
    workouts = [workout for workout in workouts if int(workout.summary.split(".")[0]) >= FIRST_WORKOUT]
    cal = Calendar(workouts)
    workouts_as_ical = cal.get_all_as_ical()
    return workouts_as_ical


if __name__ == "__main__":
    main()
