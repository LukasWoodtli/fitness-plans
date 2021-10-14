from datetime import timedelta, date

from fitness_plans.lib.workout_calendar import CalendarEvent

MON = 1
TUE = 2
WED = 3
THU = 4
FRI = 5
SAT = 6
SUN = 7

workouts = {
    MON: ("Jogging", "Intervall 20 min"),
    TUE: ("Liegestütze", "10 Wiederholungen"),
    WED: ("Rumpfbeugen", "50 Wiederholungen"),
    THU: ("Klimmzüge", "5 Wiederholungen"),
    FRI: ("Yoga", ""),
    SAT: ("Joggen", "Lang"),
    SUN: ("Joggen", "Lang"),
}


class GenericWorkoutPlan:

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def _create_workouts(self):
        current_date = self.start_date
        while current_date < self.end_date:
            week_day = current_date.isoweekday()
            current_workout = workouts[week_day]
            event = CalendarEvent(current_workout[0],
                          current_date,
                          current_workout[1])

            print(event.date)
            print(event.description)
            print(event.summary)
            current_date = current_date + timedelta(days=1)



if __name__ == "__main__":
    plan = GenericWorkoutPlan(date.today(), date.today() + timedelta(days=10))
    plan._create_workouts()