"""Simple command-line interface for medication reminders."""

from __future__ import annotations

import argparse
from datetime import datetime

from .core import generate_sample_schedule


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Display upcoming reminders from a simple medication schedule."
    )
    parser.add_argument(
        "--patient",
        default="Sample Patient",
        help="Patient name used in the sample schedule.",
    )
    parser.add_argument(
        "--at",
        dest="current_time",
        help="Current time in 'YYYY-MM-DD HH:MM' format. Defaults to now.",
    )
    parser.add_argument(
        "--window",
        type=int,
        default=60,
        help="How many upcoming minutes to inspect for reminders.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    current_time = (
        datetime.strptime(args.current_time, "%Y-%m-%d %H:%M")
        if args.current_time
        else datetime.now()
    )
    schedule = generate_sample_schedule(args.patient)
    print(schedule.format_reminders(current_time, window_minutes=args.window))


if __name__ == "__main__":
    main()
