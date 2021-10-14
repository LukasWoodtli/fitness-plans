from abc import ABC, abstractmethod


class FitnessPlan(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def read_input_file(self):
        pass

    @abstractmethod
    def create_workouts_from_input(self):
        pass

    @abstractmethod
    def filter_workouts(self):
        pass

    @abstractmethod
    def create_workout_calendar_ics(self, workouts):
        pass

    @abstractmethod
    def save_calendar(self, ics):
        pass

    def build(self):
        input = self.read_input_file()
        workouts = self.create_workouts_from_input(input)
        workouts = self.filter_workouts(workouts)
        ics = self.create_workout_calendar_ics(workouts)
        self.save_calendar(ics)
