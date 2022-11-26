#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import os
import re
from datetime import date, timedelta

from fitness_plans.lib.abstract_fitness_plan import FitnessPlan
from fitness_plans.lib.util import read_base64_file
from fitness_plans.lib.workout_calendar import CalendarEvent

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


class FitMacherFormel(FitnessPlan):
    INPUT_FILE = os.path.join(SCRIPT_DIR, 'dfmf.encoded.txt')

    def __init__(self, workout_start_date=date.today() + datetime.timedelta(days=1), first_workout=1, output_dir=None):
        super().__init__()
        self.calendar_name = "DieFitMacherFormel"
        self.workout_start = workout_start_date
        self.first_workout = first_workout
        self.output_dir = output_dir

    def get_input(self):
        return read_base64_file(self.INPUT_FILE)

    def create_workouts_from_input(self, input):
        workouts = self._split_workouts(self.get_input())
        return workouts

    def filter_workouts(self, workouts):
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
