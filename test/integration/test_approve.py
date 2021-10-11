import os
import shutil
from datetime import date
from unittest.mock import patch
from approvaltests import Options, verify, verify_file
from approvaltests.scrubbers import create_regex_scrubber

from fitness_plans.fitmacher_formel import FitMacherFormel
from fitness_plans.pullup_challenge import PullUpChallenge

OPTIONS_WITH_SCRUBBER = Options().with_scrubber(create_regex_scrubber("DTSTAMP;VALUE=DATE-TIME.*", "[creation date]"))


def test_fitmacher_formel():
    fmf = FitMacherFormel(date(2020, 5, 29))
    cal = fmf._create_workouts_from_text()
    verify(cal, options=OPTIONS_WITH_SCRUBBER)


def test_fitmacher_formel_output_file():
    test_output_dir = os.path.join(os.path.dirname(__file__), 'test_out')
    shutil.rmtree(test_output_dir, ignore_errors=True)
    fmf = FitMacherFormel(date(2021, 10, 11), output_dir=test_output_dir)
    cal = fmf.create_workout_calendar()
    out_file = os.path.join(test_output_dir, "DieFitMacherFormel.ics")
    out_file_scrubbed = out_file + ".scrubbed.ics"
    with open(out_file, "r") as o_file:
        with open(out_file_scrubbed, "w") as o_file_scrubbed:
            for line in o_file.readlines():
                if not line.startswith("DTSTAMP;VALUE=DATE-TIME"):
                    o_file_scrubbed.writelines(line)
                else:
                    o_file_scrubbed.writelines("[scrubbed creation date]\n")

    verify_file(out_file_scrubbed)


def test_pullup_challenge():
    challenge = PullUpChallenge(start_date=date(2020, 5, 30))
    calendar = challenge._create_workouts_from_text()
    verify(calendar, options=OPTIONS_WITH_SCRUBBER)


@patch('fitness_plans.fitmacher_formel.FitMacherFormel._read_input_file')
def test_create_workout_calendar(mock_read_input_file):
    mock_read_input_file.return_value = \
        "1. TAG: Hello 1\n" \
        "Workout 1\n" \
        "2. TAG: Hello 2\n" \
        "Workout 2\n" \
        "3. TAG: Hello 3\n" \
        "Workout 3"
    fmf = FitMacherFormel()
    calendar = fmf._create_workouts_from_text()
    verify(calendar, options=OPTIONS_WITH_SCRUBBER)
