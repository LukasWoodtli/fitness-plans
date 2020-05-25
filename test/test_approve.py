#!/usr/bin/env python3

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import os
import unittest
from approvaltests.approvals import verify
from approvaltests.reporters import GenericDiffReporterFactory

from fitmacher_formel.fitness import get_all_as_ical

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


class AllTests(unittest.TestCase):

    def setUp(self):
        factory = GenericDiffReporterFactory()
        factory.load(os.path.join(SCRIPT_DIR, "reporters.json"))
        self.reporter = factory.get_first_working()

    def test_add_all_to_calendar(self):
        # filter out creation timestamp
        filtered_ical = [l for l in get_all_as_ical().split("\n") if not l.startswith("DTSTAMP;VALUE=DATE-TIME")]
        verify("\n".join(filtered_ical), self.reporter)


if __name__ == '__main__':
    unittest.main()
