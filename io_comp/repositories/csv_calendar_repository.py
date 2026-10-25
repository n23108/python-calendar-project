import csv
from datetime import datetime
from typing import List

from io_comp.exceptions.calendar_exceptions import InvalidEventError
from io_comp.models.event import Event


class CsvCalendarRepository:

    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_events(self) -> List[Event]:
        """Read calendar events from the CSV file."""

        events: List[Event] = []

        with open(self.file_path, encoding="utf-8") as file:
            reader = csv.reader(file)

            for row in reader:
                if len(row) != 4:
                    raise InvalidEventError(
                        "Each CSV row must contain exactly 4 values"
                    )

                person_name = row[0].strip()
                subject = row[1].strip()
                start_time_text = row[2].strip()
                end_time_text = row[3].strip()

                try:
                    start_time = datetime.strptime(
                        start_time_text,
                        "%H:%M"
                    ).time()

                    end_time = datetime.strptime(
                        end_time_text,
                        "%H:%M"
                    ).time()

                except ValueError:
                    raise InvalidEventError(
                        f"Invalid time format for {person_name}"
                    )

                if start_time >= end_time:
                    raise InvalidEventError(
                        f"Invalid event for {person_name}: "
                        f"start time must be before end time"
                    )

                events.append(
                    Event(
                        person_name,
                        subject,
                        start_time,
                        end_time
                    )
                )

        return events