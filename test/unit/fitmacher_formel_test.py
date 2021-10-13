import os
from datetime import date

from fitness_plans.fitmacher_formel import FitMacherFormel
from fitness_plans.workout_calendar import CalendarEvent


def test_filter_skipped_workouts():
    workout_list = [
        CalendarEvent("1. TAG", date(year=1980, month=7, day=7), "description 1"),
        CalendarEvent("2. TAG", date(year=1980, month=7, day=8), "description 2"),
        CalendarEvent("3. TAG", date(year=1980, month=7, day=9), "description 3")
    ]
    fmf = FitMacherFormel(first_workout=2)
    filtered_workout_list = fmf._filter_skipped_workouts(workout_list)
    assert 2 == len(filtered_workout_list)
    assert "2. TAG" == filtered_workout_list[0].summary
    assert "3. TAG" == filtered_workout_list[1].summary


def test_split_workouts():
    text = "1. TAG: Hello 1\nWorkout 1\n"
    text += "2. TAG: Hello 2\nWorkout 2\n"
    text += "3. TAG: Hello 3\nWorkout 3\n"

    fmf = FitMacherFormel()
    workouts = fmf._split_workouts(text)
    assert 3 == len(workouts)
    for i, workout in enumerate(workouts, 1):
        expected_summary = f"{i}. TAG: Hello {i}"
        assert expected_summary == workout.summary
        expected_description = expected_summary + f"\nWorkout {i}\n"
        assert expected_description == workout.description
