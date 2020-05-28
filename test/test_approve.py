#!/usr/bin/env python3

import os
import sys

from fitmacher_formel.fitness import create_workuts_from_text

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import os
import unittest
from approvaltests.approvals import verify

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


class AllTests(unittest.TestCase):

    def test_add_all_to_calendar(self):
        # filter out creation timestamp
        filtered_ical = [l for l in create_workuts_from_text().split("\n") if not l.startswith("DTSTAMP;VALUE=DATE-TIME")]
        verify("\n".join(filtered_ical)) #, self.reporter)


if __name__ == '__main__':
    unittest.main()
