# Forex Events Scheduler

![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-Apache%202.0-blue)

This repository contains a Python script that fetches and processes Forex events from [ForexFactory's](https://www.forexfactory.com/) weekly calendar. The script is designed to run periodically, saving Forex events to structured files for easy analysis and tracking. It supports filtering events by currency, title, and impact, and allows users to save the output in either JSON or TXT format.

## Features

- **Automated Fetching**: Fetches Forex events from ForexFactory's weekly calendar every hour.
- **Event Parsing**: Extracts key details for each event, including title, currency, date, time, impact, forecast, previous value, and URL.
- **Custom Filters**: Filter events by:
  - **Currency** (e.g., USD, EUR)
  - **Title** (case-insensitive search)
  - **Impact** (e.g., High, Medium, Low)
- **Output Formats**: Save events in:
  - **JSON**: Structured and machine-readable format.
  - **TXT**: Human-readable, formatted text files.
- **Custom File Names**: Specify a custom base name for output files.
- **Scheduling**: Automatically runs the script every hour using the `schedule` library.
- **Timezone Support**: Convert event times to a specified timezone or use the system's local timezone.
- **Trading Sessions**: Identifies active trading sessions (e.g., London, New York) and highlights "Golden Time" during overlaps.
- **Configuration File**: Load options from a JSON config file for easier automation.

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

| Option              | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `--schedule`        | Schedule the script to run every hour.                                      |
| `--currency`        | Filter events by currency (e.g., `USD`, `EUR`).                             |
| `--title`           | Filter events by title (case-insensitive).                                  |
| `--impact`          | Filter events by impact (e.g., `High`, `Medium`, `Low`).                    |
| `--save-format`     | Save format: `json` or `txt` (default: `json`).                             |
| `--output-file`     | Base name for the output file (without extension, default: `filtered_events`). |
| `--timezone`        | Convert event times to the specified timezone (e.g., `America/New_York`).   |
| `--system-timezone` | Use the system's local timezone for event times.                            |
| `--config`          | Path to a JSON config file to load options from.                            |

### Examples

1. **Run Once with Default Settings**:
   ```sh
   python forex_events_scheduler.py
   ```
   Output files: `filtered_events.json` or `filtered_events.txt`.

2. **Filter by Currency and Save as TXT**:
   ```sh
   python forex_events_scheduler.py --currency USD --save-format txt --output-file usd_events
   ```
   Output file: `usd_events.txt`.

3. **Schedule the Script to Run Every Hour**:
   ```sh
   python forex_events_scheduler.py --schedule
   ```

4. **Custom File Name and Filters**:
   ```sh
   python forex_events_scheduler.py --currency USD --impact High --output-file high_impact_usd_events
   ```
   Output file: `high_impact_usd_events.json`.

5. **Convert Event Times to a Specific Timezone**:
   ```sh
   python forex_events_scheduler.py --timezone America/New_York
   ```

6. **Use System Timezone**:
   ```sh
   python forex_events_scheduler.py --system-timezone
   ```

7. **Load Configuration from a JSON File**:
   ```sh
   python forex_events_scheduler.py --config config.json
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
          "currency": "USD",
          "date": "10-27-2023",
          "time": "08:30am",
          "impact": "High",
          "forecast": "200K",
          "previous": "187K",
          "url": "https://www.forexfactory.com/event/12345",
          "sessions": ["New York", "London", "Golden Time"]
      }
  ]
  ```

- **TXT Format**:
  ```
  Title: Nonfarm Payrolls
  Currency: USD
  Date: 10-27-2023
  Time: 08:30am
  Impact: High
  Forecast: 200K
  Previous: 187K
  URL: https://www.forexfactory.com/event/12345
  Sessions: New York, London, Golden Time
  ----------------------------------------
  ```

## Configuration File Example

Change `config.json` file to store frequently used options:


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.