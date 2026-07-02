"""Core scheduling logic for the medication reminder program."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta


@dataclass(frozen=True)
class Medication:
    """A single medication plan with one or more daily dosage times."""

    name: str
    dosage: str
    times: tuple[time, ...]
    instructions: str = ""
    start_date: date | None = None
    end_date: date | None = None

    def is_active_on(self, current_date: date) -> bool:
        if self.start_date and current_date < self.start_date:
            return False
        if self.end_date and current_date > self.end_date:
            return False
        return True


@dataclass(frozen=True)
class Reminder:
    """A rendered reminder for a planned dose."""

    medication_name: str
    dosage: str
    scheduled_at: datetime
    instructions: str = ""

    @property
    def message(self) -> str:
        base_message = (
            f"Take {self.medication_name} ({self.dosage}) "
            f"at {self.scheduled_at.strftime('%H:%M')}"
        )
        if self.instructions:
            return f"{base_message} - {self.instructions}"
        return base_message


@dataclass
class MedicationSchedule:
    """Stores medications and computes reminders for a patient."""

    patient_name: str
    medications: list[Medication] = field(default_factory=list)

    def add_medication(self, medication: Medication) -> None:
        self.medications.append(medication)

    def doses_for_day(self, target_date: date) -> list[tuple[datetime, Medication]]:
        doses: list[tuple[datetime, Medication]] = []
        for medication in self.medications:
            if not medication.is_active_on(target_date):
                continue
            for dose_time in medication.times:
                doses.append((datetime.combine(target_date, dose_time), medication))
        return sorted(doses, key=lambda dose: (dose[0], dose[1].name))

    def reminders_for(
        self, current_time: datetime, window_minutes: int = 60
    ) -> list[Reminder]:
        window_end = current_time + timedelta(minutes=window_minutes)
        reminders: list[Reminder] = []
        for scheduled_at, medication in self.doses_for_day(current_time.date()):
            if current_time <= scheduled_at <= window_end:
                reminders.append(
                    Reminder(
                        medication_name=medication.name,
                        dosage=medication.dosage,
                        scheduled_at=scheduled_at,
                        instructions=medication.instructions,
                    )
                )
        return reminders

    def format_reminders(
        self, current_time: datetime, window_minutes: int = 60
    ) -> str:
        reminders = self.reminders_for(current_time, window_minutes=window_minutes)
        if not reminders:
            return (
                f"No medication is due for {self.patient_name} "
                f"in the next {window_minutes} minutes."
            )

        lines = [f"Medication reminders for {self.patient_name}:"]
        lines.extend(f"- {reminder.message}" for reminder in reminders)
        return "\n".join(lines)


def generate_sample_schedule(patient_name: str = "Sample Patient") -> MedicationSchedule:
    """Create a sample schedule for demonstration and testing."""

    return MedicationSchedule(
        patient_name=patient_name,
        medications=[
            Medication(
                name="Amoxicillin",
                dosage="500 mg",
                times=(time(8, 0), time(20, 0)),
                instructions="after food",
            ),
            Medication(
                name="Vitamin D",
                dosage="1000 IU",
                times=(time(9, 0),),
            ),
            Medication(
                name="Ibuprofen",
                dosage="200 mg",
                times=(time(13, 0),),
                instructions="only if needed",
            ),
        ],
    )
