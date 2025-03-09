# Forex Events Scheduler

![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-Apache%202.0-blue)

This repository contains a Python script that fetches and processes Forex events from [ForexFactory's](https://www.forexfactory.com/) weekly calendar. The script is designed to run periodically, saving Forex events to structured files for easy analysis and tracking. It supports filtering events by country, title, and impact, and allows users to save the output in either JSON or TXT format.

## Features

- **Automated Fetching**: Fetches Forex events from ForexFactory's weekly calendar (XML format) every hour.
- **Event Parsing**: Extracts key details for each event, including title, country, date, time, impact, forecast, previous value, and URL.
- **Custom Filters**: Filter events by:
  - **Country** (e.g., USD, EUR)
  - **Title** (case-insensitive search)
  - **Impact** (e.g., High, Medium, Low)
- **Flexible Output Formats**: Save events in:
  - **JSON**: Structured and machine-readable format.
  - **TXT**: Human-readable, formatted text files.
- **Custom File Names**: Specify a custom base name for output files.
- **Scheduling**: Automatically runs the script every hour using the `schedule` library.
- **Timezone Support**: Convert event times to a specified timezone.


## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/abbasi0abolfazl/forexfactory_calender.git
    cd forexfactory_calender
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

Run the script with the following command:

```sh
python forex_events_scheduler.py
```

### Command-Line Options

| Option           | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `--schedule`     | Schedule the script to run every hour.                                      |
| `--country`      | Filter events by country (e.g., `USD`, `EUR`).                              |
| `--title`        | Filter events by title (case-insensitive).                                  |
| `--impact`       | Filter events by impact (e.g., `High`, `Medium`, `Low`).                    |
| `--save-format`  | Save format: `json` or `txt` (default: `json`).                             |
| `--output-file`  | Base name for the output file (without extension, default: `filtered_events`). |
| `--timezone`     | Convert event times to the specified timezone (e.g., `America/New_York`).   |

### Examples

1. **Run Once with Default Settings**:
   ```sh
   python forex_events_scheduler.py
   ```
   Output files: `filtered_events.json` or `filtered_events.txt`.

2. **Filter by Country and Save as TXT**:
   ```sh
   python forex_events_scheduler.py --country USD --save-format txt --output-file usd_events
   ```
   Output file: `usd_events.txt`.

3. **Schedule the Script to Run Every Hour**:
   ```sh
   python forex_events_scheduler.py --schedule
   ```

4. **Custom File Name and Filters**:
   ```sh
   python forex_events_scheduler.py --country USD --impact High --output-file high_impact_usd_events
   ```
   Output file: `high_impact_usd_events.json`.

5. **Convert Event Times to a Specific Timezone**:
   ```sh
   python forex_events_scheduler.py --timezone America/New_York
   ```

## Running as a Background Process

To run the script as a background process, you can use `nohup` or a process manager like `systemd`:

```sh
nohup python forex_events_scheduler.py --schedule &
```

## Output Files

The script generates output files based on the provided options:
- **JSON Format**:
  ```json
  [
      {
          "title": "Nonfarm Payrolls",
          "country": "USD",
          "date": "10-27-2023",
          "time": "08:30am",
          "impact": "High",
          "forecast": "200K",
          "previous": "187K",
          "url": "https://www.forexfactory.com/event/12345",
          "sessions": ["New York"]
      }
  ]
  ```

- **TXT Format**:
  ```
  Title: Nonfarm Payrolls
  Country: USD
  Date: 10-27-2023
  Time: 08:30am
  Impact: High
  Forecast: 200K
  Previous: 187K
  URL: https://www.forexfactory.com/event/12345
  Sessions: New York
  ----------------------------------------
  ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.