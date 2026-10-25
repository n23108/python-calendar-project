from pathlib import Path
from typing import List, Protocol

from io_comp.models.event import Event
from io_comp.repositories.csv_calendar_repository import CsvCalendarRepository


class CalendarRepository(Protocol):
    def get_events(self) -> List[Event]:
        ...


def create_calendar_repository() -> CalendarRepository:
    """Create and return the repository used by the application."""

    project_root = Path(__file__).resolve().parents[2]
    csv_path = project_root / "calendar.csv"

    return CsvCalendarRepository(str(csv_path))