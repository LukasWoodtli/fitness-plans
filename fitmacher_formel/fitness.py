#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from icalendar import Calendar, Event
from datetime import date, datetime, timedelta
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../dfmf.txt')

WORKOUT_START = date.today() + timedelta(days=1) #date(year=2019, month=10, day=1)
FIRST_WORKOUT = 1

BEGIN_TEXT = "GAT .1"  # just a bit obfuscated
BEGIN_TEXT = BEGIN_TEXT[::-1]

END_TEXT = "RIM TIM MUART NENIEM EBEL"  # just a bit obfuscated
END_TEXT = END_TEXT[::-1]

SPLIT_DAY_RE = re.compile(r"([0-9]{1,2}\. TAG[^\n]*)", flags=re.M)


class iEvent:
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
        event = iEvent(title, workout_date, description)
        all_workouts.append(event)
        workout_date = workout_date + timedelta(days=1)
    return all_workouts


def add_to_calender(workout_events):
    cal = Calendar()

    cal.add('prodid', "Fitness")
    cal.add('version', '2.0')
    [event.add_to_cal(cal) for event in workout_events]

    return cal


def get_all_as_ical():
    workouts = split_workouts(read_input_file())
    workouts = [workout for workout in workouts if int(workout.summary.split(".")[0]) >= FIRST_WORKOUT]
    cal = add_to_calender(workouts)
    return cal.to_ical().decode('utf-8')


def main():
    fout = open('fitness.ics', 'w')
    fout.writelines(get_all_as_ical())
    fout.close()


if __name__ == "__main__":
    main()
