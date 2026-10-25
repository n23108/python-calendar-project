from datetime import time, timedelta
from typing import List

from io_comp.exceptions.calendar_exceptions import InvalidCalendarInputError
from io_comp.models.event import Event
from io_comp.models.time_slot import TimeSlot
from io_comp.repositories.calendar_repository import CalendarRepository
from io_comp.services.time_slot_calculator import TimeSlotCalculator


class CalendarService:

    DAY_START = time(7, 0)
    DAY_END = time(19, 0)

    def __init__(self, repository: CalendarRepository):
        self.repository = repository

    def find_available_slots(
            self,
            person_list: List[str],
            event_duration: timedelta
    ) -> List[time]:
        """Find all valid meeting start times for the requested people."""

        return self._find_available_slots_for_one_day(
            person_list,
            event_duration
        )

    def _find_available_slots_for_one_day(
            self,
            person_list: List[str],
            event_duration: timedelta
    ) -> List[time]:

        self._validate_input(person_list, event_duration)

        events = self.repository.get_events()

        free_slots = self._find_common_free_slots(
            events,
            person_list
        )

        return TimeSlotCalculator.get_available_start_times(
            free_slots,
            event_duration
        )

    def _validate_input(
            self,
            person_list: List[str],
            event_duration: timedelta
    ) -> None:
        if person_list is None:
            raise InvalidCalendarInputError(
                "person_list cannot be None"
            )

        if len(person_list) == 0:
            raise InvalidCalendarInputError(
                "person_list cannot be empty"
            )

        if event_duration is None:
            raise InvalidCalendarInputError(
                "event_duration cannot be None"
            )

        if event_duration <= timedelta(0):
            raise InvalidCalendarInputError(
                "event_duration must be greater than zero"
            )

        day_duration_minutes = (
            TimeSlotCalculator.time_to_minutes(self.DAY_END)
            - TimeSlotCalculator.time_to_minutes(self.DAY_START)
        )

        duration_minutes = TimeSlotCalculator.duration_to_minutes(
            event_duration
        )

        if duration_minutes > day_duration_minutes:
            raise InvalidCalendarInputError(
                "event_duration cannot be longer than the working day"
            )

    def _find_common_free_slots(
            self,
            events: List[Event],
            person_list: List[str]
    ) -> List[TimeSlot]:
        """Find the common free time slots for all requested people."""

        common_free_slots = [
            TimeSlot(self.DAY_START, self.DAY_END)
        ]

        for person in person_list:
            person_events = [
                event
                for event in events
                if event.person_name == person
                and event.end_time > self.DAY_START
                and event.start_time < self.DAY_END
            ]

            person_events.sort(
                key=lambda event: event.start_time
            )

            person_free_slots = TimeSlotCalculator.find_free_slots(
                person_events,
                self.DAY_START,
                self.DAY_END
            )

            common_free_slots = TimeSlotCalculator.intersect_time_slots(
                common_free_slots,
                person_free_slots
            )

            if not common_free_slots:
                return []

        return common_free_slots






