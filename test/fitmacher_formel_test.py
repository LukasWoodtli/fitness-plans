import os
import tempfile
import unittest
from datetime import date, datetime

from fitness_plans.fitmacher_formel import FitMacherFormel
from fitness_plans.workout_calendar import CalendarEvent

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


class FitmacherFormelTest(unittest.TestCase):

    def test_strip_unneeded_text(self):
        text = "1. TAG\nHello\n\nLEBE MEINEN TRAUM MIT MIR"
        stripped_text = FitMacherFormel._strip_unneeded_text(text)
        self.assertEqual(stripped_text, "1. TAG\nHello")

    def test_filter_skipped_workouts(self):

        workout_list = [
            CalendarEvent("1. TAG", date(year=1980, month=7, day=7), "description 1"),
            CalendarEvent("2. TAG", date(year=1980, month=7, day=8), "description 2"),
            CalendarEvent("3. TAG", date(year=1980, month=7, day=9), "description 3")
        ]
        fmf = FitMacherFormel(first_workout=2)
        filtered_workout_list = fmf._filter_skipped_workouts(workout_list)
        self.assertEqual(2, len(filtered_workout_list))
        self.assertEqual("2. TAG", filtered_workout_list[0].summary)
        self.assertEqual("3. TAG", filtered_workout_list[1].summary)

    def test_split_workouts(self):
        text = "1. TAG: Hello 1\nWorkout 1\n"
        text += "2. TAG: Hello 2\nWorkout 2\n"
        text += "3. TAG: Hello 3\nWorkout 3\n"

        fmf = FitMacherFormel()
        workouts = fmf._split_workouts(text)
        self.assertEqual(3, len(workouts))
        for i, workout in enumerate(workouts, 1):
            expected_summary = f"{i}. TAG: Hello {i}"
            self.assertEqual(expected_summary, workout.summary)
            expected_description = expected_summary + f"\nWorkout {i}\n"
            self.assertEqual(expected_description, workout.description)

    def test_create_workout_calendar(self):
        tempdir = tempfile.gettempdir()
        fmf = FitMacherFormel(output_dir=tempdir)
        fmf.INPUT_FILE = os.path.join(SCRIPT_DIR, "test_input.txt")
        fmf.create_workout_calendar()
        expected_output_file = os.path.join(tempdir, "DieFitMacherFormel.ics")
        self.assertTrue(os.path.isfile(expected_output_file), f"Check if file '{expected_output_file}' exists")
        self.assertGreater(os.path.getsize(expected_output_file), 0)


if __name__ == "__main__":
    unittest.main()
