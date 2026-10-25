from datetime import time, timedelta
from typing import List

import pytest

from io_comp.exceptions.calendar_exceptions import InvalidCalendarInputError
from io_comp.models.event import Event
from io_comp.services.calendar_service import CalendarService


class FakeCalendarRepository:

    def __init__(self, events: List[Event] = None):
        self.events = events if events is not None else []

    def get_events(self) -> List[Event]:
        return self.events


def test_find_available_slots_for_alice_and_jack():
    repository = FakeCalendarRepository([
        Event("Alice", "Event 1", time(8, 0), time(9, 30)),
        Event("Alice", "Event 2", time(13, 0), time(14, 0)),
        Event("Alice", "Event 3", time(16, 0), time(17, 0)),
        Event("Jack", "Event 1", time(8, 0), time(8, 50)),
        Event("Jack", "Event 2", time(9, 0), time(9, 40)),
        Event("Jack", "Event 3", time(13, 0), time(14, 0)),
    ])

    service = CalendarService(repository)

    actual = service.find_available_slots(
        ["Alice", "Jack"],
        timedelta(minutes=60)
    )

    assert actual[0] == time(7, 0)
    assert time(9, 40) in actual
    assert time(12, 0) in actual
    assert time(14, 0) in actual
    assert time(15, 0) in actual
    assert time(17, 0) in actual
    assert time(18, 0) in actual


def test_find_available_slots_when_there_are_no_events():
    repository = FakeCalendarRepository()

    service = CalendarService(repository)

    actual = service.find_available_slots(
        ["Alice"],
        timedelta(minutes=60)
    )

    assert actual[0] == time(7, 0)
    assert actual[-1] == time(18, 0)
    assert len(actual) == 661


def test_find_available_slots_with_zero_duration():
    repository = FakeCalendarRepository()

    service = CalendarService(repository)

    with pytest.raises(InvalidCalendarInputError):
        service.find_available_slots(
            ["Alice"],
            timedelta(minutes=0)
        )


def test_find_available_slots_when_person_has_no_events():
    repository = FakeCalendarRepository([
        Event("Bob", "Meeting", time(9, 0), time(10, 0))
    ])

    service = CalendarService(repository)

    actual = service.find_available_slots(
        ["Alice"],
        timedelta(minutes=60)
    )

    assert actual[0] == time(7, 0)
    assert actual[-1] == time(18, 0)
    assert len(actual) == 661


def test_find_available_slots_when_person_is_busy_all_day():
    repository = FakeCalendarRepository([
        Event("Alice", "All Day Event", time(7, 0), time(19, 0))
    ])

    service = CalendarService(repository)

    actual = service.find_available_slots(
        ["Alice"],
        timedelta(minutes=60)
    )

    assert actual == []


def test_find_available_slots_with_overlapping_events():
    repository = FakeCalendarRepository([
        Event("Alice", "Event 1", time(8, 0), time(10, 0)),
        Event("Alice", "Event 2", time(9, 0), time(11, 0))
    ])

    service = CalendarService(repository)

    actual = service.find_available_slots(
        ["Alice"],
        timedelta(minutes=60)
    )

    assert time(9, 30) not in actual
    assert time(11, 0) in actual