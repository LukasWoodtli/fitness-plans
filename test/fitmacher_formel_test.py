import unittest

from fitness_plans.fitmacher_formel import FitMacherFormel


class FitnessFormelTest(unittest.TestCase):

    def test_strip_unneeded_text(self):
        text = "1. TAG\nHello\n\nLEBE MEINEN TRAUM MIT MIR"
        stripped_text = FitMacherFormel._strip_unneeded_text(text)
        self.assertEqual(stripped_text, "1. TAG\nHello")