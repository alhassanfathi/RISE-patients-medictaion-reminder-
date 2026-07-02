"""Tests for the medication reminder program."""

from datetime import date, datetime, time
import unittest

from medication_reminder import (
    Medication,
    MedicationSchedule,
    generate_sample_schedule,
)


class MedicationScheduleTests(unittest.TestCase):
    def test_doses_for_day_are_sorted(self) -> None:
        schedule = MedicationSchedule(
            patient_name="Amina",
            medications=[
                Medication("B", "10 mg", (time(10, 0),)),
                Medication("A", "5 mg", (time(8, 0), time(10, 0))),
            ],
        )

        doses = schedule.doses_for_day(date(2026, 7, 2))

        self.assertEqual(
            [(dose_time.strftime("%H:%M"), medication.name) for dose_time, medication in doses],
            [("08:00", "A"), ("10:00", "A"), ("10:00", "B")],
        )

    def test_reminders_for_respect_window_and_activity_dates(self) -> None:
        schedule = MedicationSchedule(
            patient_name="Amina",
            medications=[
                Medication(
                    "Morning tablet",
                    "1 pill",
                    (time(8, 30),),
                    start_date=date(2026, 7, 1),
                    end_date=date(2026, 7, 3),
                ),
                Medication(
                    "Inactive tablet",
                    "1 pill",
                    (time(8, 45),),
                    end_date=date(2026, 7, 1),
                ),
                Medication("Late tablet", "1 pill", (time(10, 0),)),
            ],
        )

        reminders = schedule.reminders_for(datetime(2026, 7, 2, 8, 0), window_minutes=45)

        self.assertEqual(len(reminders), 1)
        self.assertEqual(reminders[0].medication_name, "Morning tablet")
        self.assertEqual(reminders[0].scheduled_at, datetime(2026, 7, 2, 8, 30))

    def test_format_reminders_returns_friendly_empty_message(self) -> None:
        schedule = MedicationSchedule(patient_name="Amina")

        message = schedule.format_reminders(datetime(2026, 7, 2, 8, 0), window_minutes=30)

        self.assertEqual(
            message,
            "No medication is due for Amina in the next 30 minutes.",
        )

    def test_sample_schedule_produces_readable_output(self) -> None:
        schedule = generate_sample_schedule("Amina")

        message = schedule.format_reminders(datetime(2026, 7, 2, 7, 45), window_minutes=90)

        self.assertIn("Medication reminders for Amina:", message)
        self.assertIn("Take Amoxicillin (500 mg) at 08:00 - after food", message)
        self.assertIn("Take Vitamin D (1000 IU) at 09:00", message)


if __name__ == "__main__":
    unittest.main()
