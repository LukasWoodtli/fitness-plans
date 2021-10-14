#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64
import pathlib
from datetime import date, timedelta
import re
import os

from fitness_plans.lib.abstract_fitness_plan import FitnessPlan
from fitness_plans.lib.workout_calendar import CalendarEvent, WorkoutCalendar

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


class FitMacherFormel(FitnessPlan):
    INPUT_FILE = os.path.join(SCRIPT_DIR, 'dfmf.encoded.txt')
    CALENDAR_NAME = "DieFitMacherFormel"

    def __init__(self, workout_start_date=date.today(), first_workout=1, output_dir=None):
        super().__init__()
        self.workout_start = workout_start_date
        self.first_workout = first_workout
        self.output_dir = output_dir

    def read_input_file(self):
        with open(self.INPUT_FILE, 'rb') as infile:
            encoded_data = infile.read()
            data = base64.decodebytes(encoded_data)
            data = data.decode('UTF-8')
            return data

    def create_workouts_from_input(self, input):
        workouts = self._split_workouts(self.read_input_file())
        return workouts

    def filter_workouts(self, workouts):
        return [workout for workout in workouts if int(workout.summary.split(".")[0]) >= self.first_workout]

    def create_workout_calendar_ics(self, workouts):
        cal = WorkoutCalendar(workouts)
        workouts_as_ical = cal.get_all_as_ical()
        return workouts_as_ical

    def save_calendar(self, ics):
        output_file_path = f'{self.CALENDAR_NAME}.ics'
        if self.output_dir:
            pathlib.Path(self.output_dir).mkdir(parents=True, exist_ok=True)
            output_file_path = os.path.join(self.output_dir, output_file_path)
        with open(output_file_path, 'w') as f_out:
            f_out.writelines(ics)

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

    @staticmethod
    def _create_description(description, title):
        description = re.sub("\n\n+", "\n\n", description)
        description = title + description
        return description

    def _calculate_workout_date(self, sections_index):
        return self.workout_start + (timedelta(days=1) * sections_index)


if __name__ == "__main__":
    fitmacher_formel = FitMacherFormel()
    fitmacher_formel.build()
