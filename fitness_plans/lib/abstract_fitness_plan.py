import os
import pathlib
from abc import ABC, abstractmethod

from fitness_plans.lib.workout_calendar import WorkoutCalendar


class FitnessPlan(ABC):

    def __init__(self):
        self.output_dir = None
        self.calendar_name = "Training"

    @abstractmethod
    def get_input(self):
        pass

    @abstractmethod
    def create_workouts_from_input(self, input):
        pass

    def filter_workouts(self, workouts):
        return workouts

    def create_workout_calendar_ics(self, workouts):
        cal = WorkoutCalendar(workouts)
        workouts_as_ical = cal.get_all_as_ical()
        return workouts_as_ical

    def save_calendar(self, ics):
        output_file_path = f'{self.calendar_name}.ics'
        if self.output_dir:
            pathlib.Path(self.output_dir).mkdir(parents=True, exist_ok=True)
            output_file_path = os.path.join(self.output_dir, output_file_path)
        with open(output_file_path, 'w') as f_out:
            f_out.writelines(ics)

    def build(self):
        input = self.get_input()
        workouts = self.create_workouts_from_input(input)
        workouts = self.filter_workouts(workouts)
        ics = self.create_workout_calendar_ics(workouts)
        self.save_calendar(ics)
