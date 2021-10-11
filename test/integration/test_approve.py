from datetime import date
from unittest.mock import patch
from approvaltests.approvals import verify

from fitness_plans.fitmacher_formel import FitMacherFormel
from fitness_plans.pullup_challenge import PullUpChallenge


def test_fitmacher_formel():
    # filter out creation timestamp
    fmf = FitMacherFormel(date(2020, 5, 29))
    filtered_ical = [l for l in fmf._create_workouts_from_text().split("\n") if not l.startswith("DTSTAMP;VALUE=DATE-TIME")]
    verify("\n".join(filtered_ical))


def test_pullup_challenge():
    # filter out creation timestamp
    challenge = PullUpChallenge(start_date=date(2020, 5, 30))
    calendar = challenge._create_workouts_from_text()
    filtered_ical = [l for l in calendar.split("\n") if not l.startswith("DTSTAMP;VALUE=DATE-TIME")]
    verify("\n".join(filtered_ical))


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
    filtered_ical = [l for l in calendar.split("\n") if not l.startswith("DTSTAMP;VALUE=DATE-TIME")]
    verify("\n".join(filtered_ical))
