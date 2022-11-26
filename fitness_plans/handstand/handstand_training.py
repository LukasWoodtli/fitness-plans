import os
from datetime import date, timedelta

from fitness_plans.lib.abstract_fitness_plan import FitnessPlan
from fitness_plans.lib.workout_calendar import CalendarEvent

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

WORKOUT = [
    "Mobilisieren, Stärken und Dehnen",
    "",
    "Handgelenke, Schultern und Arme",
    "",
    "Nacken",
    "",
    "Halbkreise mit dem Nacken (Seite 57) – 5 Wiederholungen von Seite zu Seite",
    #"Halber Kopfstand (Seite 58) – 5 Atemzüge",
    #"Seitlicher Nackenstretch (Seite 59) – 3–5 tiefe Atemzüge pro Seite",
    "",
    "Core",
    "",
    "Katze und Kuh (Seite 60) – 5 Atemzüge",
    #"Diagonale Crunches (Seite 66) – 20 Wiederholungen",
    #"Tuck Rocks (Seite 68) – 10 Wiederholungen",
    #"Straight Leg Lifts (Seite 64) – 10 Wiederholungen",
    #"Optional: Dynamische Schulterbrücke (Seite 61) – 5 Atemzüge",
    "",
    "Beine",
    "",
    "Fuß- und Beingelenke mobilisieren (Seite 74) – 30 Sekunden",
    #"Squat Hold (Seite 76) – 30 Sekunden",
    #"Aktive Flexibilität in der sitzenden Grätsche (Seite 77) – 2 Runden à 10 Sekunden optional je eine Runde mit einzelnem Bein",
    #"Pancake Stretch (Seite 81) – 30 Sekunden",
    #"Halber Spagat (Seite 83) – 30 Sekunden pro Seite",
    #"Frog Stretch (Seite 86) – 30 Sekunden",
    #"Handstandtraining",
    #"Straddle Jumping Jacks (Seite 222) – 5 Wiederholungen",
    "",
    "Ausrichtung",
    "",
    "Alignment Drill auf dem Boden liegend (Seite 133) – 2 Runden à 10 Sekunden",
    "",
    "An der Wand",
    "",
    #"Mit Rücken zur Wand: Kick-up in den Handstand, optional vom Stehen aus oder mit den Händen am Boden starten (Seite 190) – 3 Wiederholungen",
    #"Mit Bauch zur Wand: Ausdauersets (Seite 119) – 3 Runden à 30 Sekunden, 20 Sekunden und 10 Sekunden",
    #"L-Shape mit einem Bein für die Ausrichtung (Seite 117) – 10 Sekunden pro Bein",
    #"L-Shape mit beiden Beinen für obere Rücken- und Schultermuskulatur (Seite 118) – 10 Sekunden",
    #"Handstand-Balanceübungen an der Wand mit Formen deiner Wahl – 1–2 Runden",
    "",
    "Frei im Raum",
    "",
    "Krähe, die großen Zehen berühren sich (Seite 152) – 5 tiefe Atemzüge",
    #"Die folgenden Übungen wahlweise im Kopfstand oder FeetUp",
    #"Gerade Linie finden – 10 Sekunden stabil halten",
    #"Tuck-Variationen: Mini, Medium, Full (Seite 168) – je 1 Runde à 3–5 Wiederholungen; im wöchentlichen Wechsel mit Straddle-Variationen: Mini, Medium, Full (Seite 165) – je 1 Runde à 3–5 Wiederholungen",
    #"Tuck Leg Presses (Seite 205) – 5–10 Wiederholungen; im wöchentlichen Wechsel mit 1 Runde 5–10 Mal Tuck Leg Presses",
    #"Handstand: Hochkicken mit Bailout (Seite 188) – 3 Wiederholungen. ACHTUNG: Beginne diese Übung mit einer Hilfestellung. Praktiziere sie erst allein, wenn du die Übung kennst und dich sicher fühlst!",
    "",
    "Cool-down",
    "",
    "Unterarmmassage im Squat (Seite 36) – 5 tiefe Atemzüge",
    #"Handgelenke dehnen: Unterarmrückseite (Seite 32) – 5 tiefe Atemzüge",
    #"Kamel und Twist (Seite 52) – 5 Atemzüge",
    #"Vorwärtsbeuge (Seite 80) – 5 Atemzüge",
    ]

class HandStand(FitnessPlan):
    CALENDAR_NAME = "Handstand"
    WORKOUT_FREQUENCY = timedelta(days=2)

    def __init__(self,
                 workout_start_date=date.today() + timedelta(days=1),
                 workout_length=timedelta(weeks=2)):
        super().__init__()
        self.workout_start_date = workout_start_date
        self.workout_end_date = self.workout_start_date + workout_length

    def get_input(self):
        return WORKOUT

    def create_workouts_from_input(self, input):
        events = []
        current_day = self.workout_start_date
        while current_day < self.workout_end_date:
            events.append(CalendarEvent("Handstand", current_day, "\n".join(WORKOUT)))
            current_day += self.WORKOUT_FREQUENCY
        return events


if __name__ == '__main__':  # pragma: no cover
    h = HandStand()
    h.build()
