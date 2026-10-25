# Comp In-Office Coding Evaluation - Python

Python implementation of the calendar coding exercise.

## Getting Started

### Prerequisites

Python 3.8 or higher is required.

### Setup

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Install the package in development mode:

```bash
pip install -e .
```

## Running the Application

Run the application with:

```bash
python -m io_comp.app
```

When the application is run without command-line arguments, it asks the user to enter:

- The names of the people who should attend the meeting.
- The desired meeting duration in minutes.

Example:

```text
Enter people names separated by commas: Alice, Jack
Enter meeting duration in minutes: 60
```

The application then calculates and displays the available meeting times.

The application can also be run using the installed console script:

```bash
comp-calendar
```

## Command-Line Arguments

The application also supports command-line arguments.

Specify the people:

```bash
python -m io_comp.app --people Alice Jack
```

Specify the meeting duration:

```bash
python -m io_comp.app --duration 60
```

Both options can be combined:

```bash
python -m io_comp.app --people Alice Jack --duration 60
```

### JSON Output

Available meeting start times can also be returned as JSON:

```bash
python -m io_comp.app --people Alice Jack --duration 60 --json
```

## Running Tests

Run all tests with:

```bash
pytest
```

For detailed test output:

```bash
pytest -v
```

## Project Structure

```text
CalendarProject/
├── io_comp/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── event.py
│   │   └── time_slot.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── calendar_repository.py
│   │   └── csv_calendar_repository.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── calendar_service.py
│   │   └── time_slot_calculator.py
│   ├── exceptions/
│   │   ├── __init__.py
│   │   └── calendar_exceptions.py
│   ├── __init__.py
│   └── app.py
├── tests/
│   └── test_calendar_service.py
├── calendar.csv
├── requirements.txt
├── setup.py
└── README.md
```

## Architecture

The application is divided into separate components with clear responsibilities:

- **Models** represent calendar data, including `Event` and `TimeSlot`.
- **Repositories** are responsible for loading calendar events from the CSV file.
- **Services** contain the main calendar logic for finding common available meeting times.
- **TimeSlotCalculator** performs calculations related to time slots, such as finding free slots and intersecting time ranges.
- **Exceptions** contain custom exceptions used for invalid calendar input and invalid events.
- **App** is the entry point of the application and handles user input and output.

This separation keeps the code modular, readable, and easier to maintain and extend.

## Calendar Functionality

The application finds all possible starting times for a meeting based on:

- A list of people who should attend.
- The desired meeting duration.

The calendar represents one working day from:

```text
07:00 - 19:00
```

Calendar events are loaded from `calendar.csv`.

## Calendar File Format

The CSV file contains four values per event:

```text
Person name, Event subject, Event start time, Event end time
```

Example:

```text
Alice,"Morning meeting",08:00,09:30
Alice,"Lunch with Jack",13:00,14:00
Jack,"Morning meeting",08:00,08:50
```

## Main Method

The main calendar operation is:

```python
from datetime import time, timedelta
from typing import List


def find_available_slots(
    person_list: List[str],
    event_duration: timedelta
) -> List[time]:
    ...
```

The method returns all possible meeting start times at which all requested people are available for the specified duration.