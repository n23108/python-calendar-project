from datetime import time, timedelta
from typing import List

from io_comp.models.event import Event
from io_comp.models.time_slot import TimeSlot


class TimeSlotCalculator:

    @staticmethod
    def duration_to_minutes(event_duration: timedelta) -> int:
        total_seconds = event_duration.total_seconds()

        minutes = int(total_seconds // 60)

        if total_seconds % 60 != 0:
            minutes += 1

        return minutes

    @staticmethod
    def time_to_minutes(value: time) -> int:
        return value.hour * 60 + value.minute

    @staticmethod
    def minutes_to_time(total_minutes: int) -> time:
        hours = total_minutes // 60
        minutes = total_minutes % 60

        return time(hours, minutes)

    @staticmethod
    def max_time(first: time, second: time) -> time:
        if first > second:
            return first

        return second

    @staticmethod
    def min_time(first: time, second: time) -> time:
        if first < second:
            return first

        return second

    @staticmethod
    def intersect_time_slots(
            first_slots: List[TimeSlot],
            second_slots: List[TimeSlot]
    ) -> List[TimeSlot]:
        """Find intersections between two lists of free time slots."""

        intersections: List[TimeSlot] = []

        first_index = 0
        second_index = 0

        while (
                first_index < len(first_slots)
                and second_index < len(second_slots)
        ):
            first_slot = first_slots[first_index]
            second_slot = second_slots[second_index]

            intersection_start = TimeSlotCalculator.max_time(
                first_slot.start_time,
                second_slot.start_time
            )

            intersection_end = TimeSlotCalculator.min_time(
                first_slot.end_time,
                second_slot.end_time
            )

            if intersection_start < intersection_end:
                intersections.append(
                    TimeSlot(
                        intersection_start,
                        intersection_end
                    )
                )

            if first_slot.end_time < second_slot.end_time:
                first_index += 1
            elif second_slot.end_time < first_slot.end_time:
                second_index += 1
            else:
                first_index += 1
                second_index += 1

        return intersections

    @staticmethod
    def find_free_slots(
            relevant_events: List[Event],
            day_start: time,
            day_end: time
    ) -> List[TimeSlot]:
        """Find free time slots within the working day."""

        free_slots: List[TimeSlot] = []

        if len(relevant_events) == 0:
            return [TimeSlot(day_start, day_end)]

        first_event = relevant_events[0]

        first_start = TimeSlotCalculator.max_time(
            first_event.start_time,
            day_start
        )

        first_end = TimeSlotCalculator.min_time(
            first_event.end_time,
            day_end
        )

        if first_start > day_start:
            free_slots.append(
                TimeSlot(day_start, first_start)
            )

        current_end = first_end

        for event in relevant_events[1:]:
            event_start = TimeSlotCalculator.max_time(
                event.start_time,
                day_start
            )

            event_end = TimeSlotCalculator.min_time(
                event.end_time,
                day_end
            )

            if event_start <= current_end:
                if event_end > current_end:
                    current_end = event_end
            else:
                free_slots.append(
                    TimeSlot(current_end, event_start)
                )
                current_end = event_end

        if current_end < day_end:
            free_slots.append(
                TimeSlot(current_end, day_end)
            )

        return free_slots

    @staticmethod
    def get_available_start_times(
            free_slots: List[TimeSlot],
            event_duration: timedelta
    ) -> List[time]:
        """Return all valid meeting start times for the given duration."""

        available_start_times: List[time] = []

        duration_minutes = TimeSlotCalculator.duration_to_minutes(
            event_duration
        )

        for slot in free_slots:
            start_minutes = TimeSlotCalculator.time_to_minutes(
                slot.start_time
            )

            end_minutes = TimeSlotCalculator.time_to_minutes(
                slot.end_time
            )

            slot_duration = end_minutes - start_minutes

            if slot_duration >= duration_minutes:
                latest_start = end_minutes - duration_minutes
                current_start = start_minutes

                while current_start <= latest_start:
                    available_start_times.append(
                        TimeSlotCalculator.minutes_to_time(
                            current_start
                        )
                    )

                    current_start += 1

        return available_start_times