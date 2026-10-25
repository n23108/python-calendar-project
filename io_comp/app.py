import argparse
import json
import logging
import sys
from datetime import time, timedelta
from itertools import groupby
from typing import List, Tuple

from io_comp.repositories.calendar_repository import (
    create_calendar_repository
)
from io_comp.services.calendar_service import CalendarService


logger = logging.getLogger(__name__)


def time_to_minutes(value: time) -> int:
    return value.hour * 60 + value.minute


def print_available_ranges(
        available_slots: List[time],
        event_duration: timedelta
) -> None:
    if not available_slots:
        logger.info("No available slots")
        return

    grouped_slots = groupby(
        enumerate(available_slots),
        key=lambda item: time_to_minutes(item[1]) - item[0]
    )

    for _, group in grouped_slots:
        group_list = list(group)

        start_time = group_list[0][1]
        last_start_time = group_list[-1][1]

        if start_time == last_start_time:
            logger.info(
                f"Starting Time of available slots: "
                f"{start_time.strftime('%H:%M')}"
            )
        else:
            print_range(start_time, last_start_time)


def minutes_to_time(total_minutes: int) -> time:
    hours = total_minutes // 60
    minutes = total_minutes % 60

    return time(hours, minutes)


def print_range(start_time: time, end_time: time) -> None:
    start_text = start_time.strftime("%H:%M")
    end_text = end_time.strftime("%H:%M")

    if time_to_minutes(end_time) - time_to_minutes(start_time) == 0:
        logger.info(
            f"Starting Time of available slots: {start_text}"
        )
    else:
        logger.info(
            f"Starting Time of available slots: "
            f"{start_text} - {end_text}"
        )


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Find common available calendar slots"
    )

    parser.add_argument(
        "--people",
        nargs="+",
        default=["Alice", "Jack"],
        help="Names of people to include"
    )

    parser.add_argument(
        "--duration",
        type=int,
        default=60,
        help="Meeting duration in minutes"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output available slots as JSON"
    )

    return parser.parse_args()


def get_user_input() -> Tuple[List[str], int]:
    people_input = input(
        "Enter people names separated by commas: "
    )

    people = [
        name.strip()
        for name in people_input.split(",")
        if name.strip()
    ]

    while True:
        try:
            duration = int(
                input("Enter meeting duration in minutes: ")
            )

            if duration <= 0:
                logger.error(
                    "Meeting duration must be greater than 0."
                )
                continue

            return people, duration

        except ValueError:
            logger.error(
                "Please enter a valid number."
            )


def main() -> None:
    """Run the calendar application."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s"
    )

    args = parse_arguments()

    if len(sys.argv) == 1:
        people, duration = get_user_input()
    else:
        people = args.people
        duration = args.duration

    repository = create_calendar_repository()
    service = CalendarService(repository)

    event_duration = timedelta(minutes=duration)

    available_slots = service.find_available_slots(
        people,
        event_duration
    )

    if args.json:
        logger.info(
            json.dumps(
                [
                    slot.strftime("%H:%M")
                    for slot in available_slots
                ]
            )
        )
    else:
        print_available_ranges(
            available_slots,
            event_duration
        )


if __name__ == "__main__":
    main()