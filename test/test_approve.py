#!/usr/bin/env python3

import os
import sys
from datetime import date, timedelta

from fitness_plans.fitmacher_formel import FitMacherFormel
from fitness_plans.pullup_challenge import get_calendar_as_string

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import os
import unittest
from approvaltests.approvals import verify

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


class AllTests(unittest.TestCase):

    def test_fitmacher_formel(self):
        # filter out creation timestamp
        fmf = FitMacherFormel(date.today() + timedelta(days=1))
        filtered_ical = [l for l in fmf._create_workouts_from_text().split("\n") if not l.startswith("DTSTAMP;VALUE=DATE-TIME")]
        verify("\n".join(filtered_ical))

    def test_pullup_challenge(self):
        # filter out creation timestamp
        calender = get_calendar_as_string()
        filtered_ical = [l for l in calender.split("\n") if not l.startswith("DTSTAMP;VALUE=DATE-TIME")]
        verify("\n".join(filtered_ical))

if __name__ == '__main__':
    unittest.main()
