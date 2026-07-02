# RISE-patients-medictaion-reminder-

Python programme that manages a simple medication schedule and reminds patients when to take their medication.

## Features

- models medications with dosage, daily intake times and optional instructions
- builds a simple medication schedule for a patient
- uses `datetime` to find reminders due in a configurable time window
- includes a small command-line interface for viewing sample reminders
- ships with unit tests for the scheduling and reminder logic

## Installation

This project uses only the Python standard library.

```bash
python -m unittest discover -s tests -v
```

## Usage

Run the sample reminder programme:

```bash
python -m medication_reminder --patient "Amina" --at "2026-07-02 07:45" --window 90
```

Example output:

```text
Medication reminders for Amina:
- Take Amoxicillin (500 mg) at 08:00 - after food
- Take Vitamin D (1000 IU) at 09:00
```

## Architecture overview

- `medication_reminder/core.py` contains the data structures and scheduling logic
- `medication_reminder/cli.py` contains the user interface for the command line
- `tests/test_medication_reminder.py` validates the core reminder behaviour
