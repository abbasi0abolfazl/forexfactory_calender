# Forex Events Scheduler

This repository contains a Python script that fetches and processes Forex events from ForexFactory's weekly calendar. The script runs every hour and saves all events and high-impact USD events to separate text files.

## Features

- Fetches Forex events from ForexFactory's weekly calendar (XML format).
- Parses the XML data and extracts relevant information for each event.
- Saves all events and high-impact USD events to separate text files.
- Runs the fetching and parsing process every hour using the `schedule` library.

## Prerequisites
- Python 3.x

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/abbasi0abolfazl/forexfactory_calender.git
    cd forex-events-scheduler
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the script:
    ```sh
    python forex_events_scheduler.py
    ```

2. The script will fetch and process the Forex events every hour and save the results in text files named `all_events_this_week_<formatted_monday>.txt` and `high_impact_events_this_week_<formatted_monday>.txt`, where `<formatted_monday>` is the date of the current Monday in `MM-DD-YYYY` format.

## Running as a Background Process

To run the script as a background process, you can use a process manager like `nohup` or run it inside a screen session:

```sh
nohup python3 forex_events_scheduler.py &
```

