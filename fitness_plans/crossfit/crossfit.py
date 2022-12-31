#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64
import datetime
import json
import os
import re
from datetime import date, timedelta

from fitness_plans.lib.abstract_fitness_plan import FitnessPlan
from fitness_plans.lib.util import read_base64_file
from fitness_plans.lib.workout_calendar import CalendarEvent

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


class CrossFit(FitnessPlan):

    def __init__(self, workout_start_date=date.today() + datetime.timedelta(days=1), first_workout=1, output_dir=None):
        super().__init__()
        self.calendar_name = "Cross Fit"
        self.workout_start = workout_start_date
        self.first_workout = first_workout
        self.output_dir = output_dir

    def get_input(self):
        ret_encoded = b'ewogICIxIjogIkVNT1RNIGZcdTAwZmNyIDUgTWludXRlbjogMTUgQWlyIFNxdWF0c1xuQXVmIFplaXQ6IDEwLi4uM' \
              b'SBQdXNoLVVwIHVuZCBTaXQtVXAiLAogICI0IjogIkVNT1RNIGZcdTAwZmNyIDUgTWludXRlbjpcbjE1IFJ1c3NpYW4' \
              b'gU3dpbmdzXG5BdWYgWmVpdDogMjUwIFJvcGUgSnVtcHMiLAogICI2IjogIjEwLi4uMSBHb2JsZXQgU3F1YXRzICYgU' \
              b'HVzaC1VcHNcbkludGVydmFsbGUgRkxSIiwKICAiOCI6ICJQdWxsLVVwc1xuQXVmIFplaXQ6IDE1IC0gMTIgLSA5IFB1c' \
              b'2gtVXBzLFxuUnVzc2lhbiBTd2luZ3MsXG5TaXQtVXBzIiwKICAiMTEiOiAiNjAgU2VrdW5kZW4gQU1SQVA6IEJ1cnBlZX' \
              b'NcbkF1ZiBaZWl0OlxuNDAwIFJvcGUgSnVtcHNcbkludGVydmFsbGUgRkxSIiwKICAiMTMiOiAiRU1PVE0gZlx1MDBmY3' \
              b'IgNSBNaW51dGVuOiAxMiBBbWVyaWNhbiBTd2luZ3NcbjcgTWludXRlbiBBTVJBUDpcbjUgUHVzaC1VcHNcbjEwIFNpdC1' \
              b'VcHNcbjE1IEFpci1TcXVhdHMiLAogICIxNSI6ICI0eCBtYXguIFB1bGwtVXBzXG5BdWYgWmVpdDogMTAwMCBSb3BlI' \
              b'Ep1bXBzIHVuZCAxMDAgUHVzaC1VcHNcbjIgTWludXRlbiBIb2xsb3cgSG9sZCIsCiAgIjE4IjogIkVNT1RNIGZcdTAw' \
              b'ZmNyIDggTWludXRlbjpcbmdlcmFkZTogMTIgUnVzc2lhbiBTd2luZ3NcbnVuZ2VyYWRlOiAxMCBBbWVyaWNhbiBTd2luZ3' \
              b'NcblxuOCBSdW5kZW4gVGFiYXRhIEFpciBTcXVhdHMiLAogICIyMCI6ICI4IFJ1bmRlbiBUYWJhdGEgUm9wZSBKdW1wc1xuOC' \
              b'B4IDEwIG0gT25lIEFybSBPdmVyaGVhZCBMdW5nZXMiLAogICIyMiI6ICI0eCBtYXguIFB1c2gtdXBzXG5FTU9UTSBmXHUwMGZj' \
              b'ciAxMiBNaW51dGVuOlxuZ2VyYWRlOiAxMiBHb2JsZXQgU3F1YXRzXG51bmdlcmFkZTogMTAgUnVzc2lhbiBTd2luZ3NcblxuNCBS' \
              b'dW5kZW4gRkxSL01vdW50YWluIENsaW1iZXIgRmluaXNoZXIvRkxSIiwKICAiMjUiOiAiRU1PVE0gZlx1MDBmY3IgNSBNaW51dG' \
              b'VuOiBQdWxsLXVwc1xuOCBSdW5kZW4gVGFiYXRhIEJ1cnBlZXNcbjEyMCBTZWt1bmRlbiBMLUhvbGQiLAogICIyNyI6ICI0eCBtYXg' \
              b'uIFB1bGwtdXBzXG5cbkVNT1RNIGZcdTAwZmNyIDIwIE1pbnV0ZW46XG41IFB1c2gtdXBzLFxuNSBSdXNzaWFuIFN3aW5ncyxcbjUgU' \
              b'2l0LXVwcyIsCiAgIjI5IjogIjEwIE1pbnV0ZW4gUm9wZSBKdW1wc1xuRU1PVE0gZlx1MDBmY3IgMTAgTWludXRlbjpcbmdlcmFkZTo' \
              b'gMTAgR29ibGV0IFNxdWF0c1xudW5nZXJhZGU6IEhvbGxvdyBIb2xkIC9GTFIiLAogICIzMSI6ICJDaW5keVxuMTgwIFNla3VuZGVuI' \
              b'EwtU2l0LCBMLUhhbmcgdW5kIEhvbGxvdyBIb2xkIiwKICAiMzMiOiAiTHVuZ2VzLVZhcmlhdGlvbmVuLCBkYXp3aXNjaGVuIG1heCB' \
              b'QdWxsLXVwc1xuMkRlYXRoIGJ5IEJ1cnBlZXMiLAogICIzNSI6ICJBTVJBUCBmXHUwMGZjciA1IE1pbnV0ZW46XG42IFNESFAgJiA2' \
              b'IEJveCBKdW1wc1xuQXVmIFplaXQ6IDIxIC0gMTUgLSA5IEFtZXJpY2FuIFN3aW5ncyAmIFB1c2gtdXBzIiwKICAiMzciOiAiNiB4I' \
              b'DEwIEtldHRsZWJlbGwgRnJvbnQgU3F1YXRzLFxuZGF6d2lzY2hlbiBKdW1waW5nIFB1bGwtdXBzXG5cbjIxIC0gMTUgLSA5OiBEb3V' \
              b'ibGUgVW5kZXJzICYgQnVycGVlcyBvZGVyIFNpbmdsZXNcbnVuZCBCdXJwZWVzIGltIFdlY2hzZWxcblxuNCBSdW5kZW46IEZMUi9N' \
              b'b3VudGFpbiBDbGltYmVycy9GTFIiLAogICIzOSI6ICI0eCBtYXguIFB1bGwtdXBzXG5BTVJBUCBmXHUwMGZjciAxMCBNaW51dGVuO' \
              b'lxuNSBQdXNoLXVwc1xuMTAgQW1lcmljYW4gU3dpbmdzXG4xNSBTaXQtdXBzXG4iLAogICI0MSI6ICI1MDAwLW0tTGF1ZlxuMyB4ID' \
              b'EwIEhvbGxvdyBSb2NrLFxuZGF6d2lzY2hlbiAyIHggNDUgU2VrdW5kZW4gU3VwZXJtYW5cbiIsCiAgIjQzIjogIjIgUnVuZGVuOiB' \
              b'Nb3VudGFpbiBDbGltYmVycy9GTFIvTW91bnRhaW5cbkNsaW1iZXJzL0ZMUlxuQXVmIFplaXQ6IDEwMCBCdXJwZWVzXG4iLAogICI0N' \
              b'SI6ICIxMCBNaW51dGVuIFJvcGUgSnVtcDtcbjMgeCAxMiBIb2xsb3cgUm9ja1xuNSBSdW5kZW46XG5tYXguIFB1c2gtdXBzXG4xMCB' \
              b'Cb3ggSnVtcHNcbjUwIFNpbmdsZXMgdW5icm9rZW5cbiIsCiAgIjQ3IjogIjMgRHVyY2hnXHUwMGU0bmdlIFB1bGwtdXBzXG5FTU9UT' \
              b'SBmXHUwMGZjciA4IE1pbnV0ZW46IEFtZXJpY2FuIFN3aW5nc1xuRU1PVE0gZlx1MDBmY3IgOCBNaW51dGVuOiBIb2xsb3cgUm9ja1x' \
              b'uRU1PVE0gZlx1MDBmY3IgOCBNaW51dGVuOiBHb2JsZXQgTHVuZ2VzXG4iLAogICI0OSI6ICIxMCBNaW51dGVuIFJvcGUgSnVtcFxuN' \
              b'yBNaW51dGVuIEFNUkFQOlxuNSBQdXNoLXVwc1xuMTAgU2l0LXVwc1xuMTUgQWlyIFNxdWF0c1xuIiwKICAiNTEiOiAiNHggbWF4LiB' \
              b'QdWxsLXVwc1xuNSBSdW5kZW46XG42MCBTZWt1bmRlbiBBTVJBUDpcbjMgQnVycGVlc1xuNSBBbWVyaWNhbiBTd2luZ3NcbiIsCiAg' \
              b'IjUzIjogIjUgTWludXRlbiBSb3BlIEp1bXBzXG5FTU9UTSBmXHUwMGZjciAzMCBNaW51dGVuOlxuNSBQdXNoLXVwc1xuNSBSdXNza' \
              b'WFuIFN3aW5nc1xuNSBTaXQtdXBzXG5KZWRlIDUuIE1pbnV0ZTogMTAgQnVycGVlc1xuIiwKICAiNTUiOiAiNSBNaW51dGVuIFJvcG' \
              b'UgSnVtcHNcbjIgTWludXRlbiBBTVJBUDogRG91YmxlIFVuZGVyc1xuNHggbWF4LiBIb2xsb3cgSG9sZFxuOCBSdW5' \
              b'kZW4gVGFiYXRhIEJ1cnBlZXMiCn0='

        ret = base64.b64decode(ret_encoded).decode(encoding="utf-8")
        ret = json.loads(ret)
        ret = {int(i): j for i, j in ret.items()}

        return ret

    def create_workouts_from_input(self, input):
        workouts = []
        for day, workout in input.items():
            workouts.append(
                CalendarEvent(f"Workout Day {day}",
                              self._calculate_workout_date(day),
                              workout))

        return workouts

    def _calculate_workout_date(self, sections_index):
        return self.workout_start + (timedelta(days=1) * sections_index)


if __name__ == "__main__":
    cross_fit = CrossFit()
    cross_fit.build()
