#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import date, timedelta
import re
import os

from fitmacher_formel.workout_calendar import CalendarEvent, WorkoutCalendar

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def main():
    fout = open('fitness.ics', 'w')
    dfmf = FitmacherFormel()
    workouts_as_ical = dfmf.create_workouts_from_text()
    fout.writelines(workouts_as_ical)
    fout.close()


class FitmacherFormel:
    INPUT_FILE = os.path.join(SCRIPT_DIR, '../dfmf.txt')

    def __init__(self, workout_start_date=date.today(), first_workout=1):
        self.workout_start = workout_start_date
        self.first_workout = first_workout

    def create_workouts_from_text(self):
        workouts = self._split_workouts(self._read_input_file())
        workouts = self._filter_skipped_workouts(workouts)
        cal = WorkoutCalendar(workouts)
        return cal.get_all_as_ical()

    def _read_input_file(self):
        with open(self.INPUT_FILE, 'r', encoding='utf-8') as infile:
            data = infile.read()
            data = self._strip_unneeded_text(data)
            return data

    @staticmethod
    def _strip_unneeded_text(data):
        data = FitmacherFormel._strip_unneeded_begin_of_text(data)
        data = FitmacherFormel._strip_unneeded_end_of_text(data)
        return data

    @staticmethod
    def _strip_unneeded_end_of_text(data):
        end_text = "RIM TIM MUART NENIEM EBEL"  # just a bit obfuscated
        end_text = end_text[::-1]
        data = data.split(end_text)[0]  # remove end
        return data

    @staticmethod
    def _strip_unneeded_begin_of_text(data):
        begin_text = "GAT .1"  # just a bit obfuscated
        begin_text = begin_text[::-1]
        data = data[data.find(begin_text):]  # remove begin
        return data

    def _filter_skipped_workouts(self, workouts):
        return [workout for workout in workouts if int(workout.summary.split(".")[0]) >= self.first_workout]

    def _split_workouts(self, data):
        split_day_re = r"([0-9]{1,2}\. TAG[^\n]*)"

        all_workouts = []
        sections = re.split(split_day_re, data, flags=re.M)
        sections = sections[1:]  # first entry is empty
        assert len(sections) % 2 == 0
        for s in range(0, int(len(sections)/2)):
            event = self._create_workout_event(s, sections)
            all_workouts.append(event)
        return all_workouts

    def _create_workout_event(self, sections_index, sections):
        title_index = sections_index * 2
        title = sections[title_index]
        description = sections[title_index + 1]
        description = self._create_description(description, title)
        workout_date = self._calculate_workout_date(sections_index)
        event = CalendarEvent(title, workout_date, description)
        return event

    def _create_description(self, description, title):
        description = re.sub("\n\n+", "\n\n", description)
        description = title + description
        return description

    def _calculate_workout_date(self, sections_index):
        return self.workout_start + (timedelta(days=1) * sections_index)


if __name__ == "__main__":
    main()
