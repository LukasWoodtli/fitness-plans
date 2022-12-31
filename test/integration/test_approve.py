import os
import shutil
from datetime import date
from unittest.mock import patch

from approvaltests import Options, verify, verify_file
from approvaltests.scrubbers import create_regex_scrubber

from fitness_plans.crossfit.crossfit import CrossFit
from fitness_plans.dfmf.fitmacher_formel import FitMacherFormel
from fitness_plans.pullup_challenge import PullUpChallenge
from fitness_plans.push_ups import PushUps

OPTIONS_WITH_SCRUBBER = Options()\
    .for_file.with_extension(".txt")\
    .with_scrubber(create_regex_scrubber("DTSTAMP;VALUE=DATE-TIME.*", "[creation date]"))


@patch('fitness_plans.dfmf.fitmacher_formel.FitMacherFormel.save_calendar')
def test_fitmacher_formel(mock_save_calendar):
    fmf = FitMacherFormel(date(2020, 5, 29))
    fmf.build()
    cal = mock_save_calendar.call_args.args[0]
    verify(cal, options=OPTIONS_WITH_SCRUBBER)


def test_fitmacher_formel_output_file():
    test_output_dir = os.path.join(os.path.dirname(__file__), 'test_out')
    fmf = FitMacherFormel(date(2021, 10, 11), output_dir=test_output_dir)
    fmf.build()
    out_file = os.path.join(test_output_dir, "DieFitMacherFormel.ics")

    verify_file(out_file, options=OPTIONS_WITH_SCRUBBER)

def test_cross_fit_output_file():
    test_output_dir = os.path.join(os.path.dirname(__file__), 'test_out')
    cross_fit = CrossFit(date(2022, 12, 11), output_dir=test_output_dir)
    cross_fit.build()
    out_file = os.path.join(test_output_dir, "Cross Fit.ics")

    verify_file(out_file, options=OPTIONS_WITH_SCRUBBER)

def test_pullup_challenge():
    challenge = PullUpChallenge(start_date=date(2020, 5, 30))
    calendar = challenge._create_workouts_from_text()
    verify(calendar, options=OPTIONS_WITH_SCRUBBER)


def test_pushups():
    push_ups = PushUps(start_date=date(2020, 5, 30))
    calendar = push_ups._create_workouts()
    verify(calendar, options=OPTIONS_WITH_SCRUBBER)


@patch('fitness_plans.dfmf.fitmacher_formel.FitMacherFormel.save_calendar')
@patch('fitness_plans.dfmf.fitmacher_formel.FitMacherFormel.get_input')
def test_create_workout_calendar(mock_read_input_file, mock_save_calendar):
    mock_read_input_file.return_value = \
        "1. TAG: Hello 1\n" \
        "Workout 1\n" \
        "2. TAG: Hello 2\n" \
        "Workout 2\n" \
        "3. TAG: Hello 3\n" \
        "Workout 3"
    fmf = FitMacherFormel(workout_start_date=date(2021, 10, 11))
    fmf.build()
    calendar = mock_save_calendar.call_args.args[0]
    verify(calendar, options=OPTIONS_WITH_SCRUBBER)
