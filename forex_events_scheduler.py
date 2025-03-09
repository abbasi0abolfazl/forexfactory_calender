import json
import time
from datetime import datetime, timedelta

import click
import pytz
import requests
import schedule as scheduler
import xml.etree.ElementTree as ET


URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"
SESSIONS = {
    "Sydney": {"start": "21:00", "end": "06:00"},
    "Tokyo": {"start": "00:00", "end": "09:00"},
    "London": {"start": "07:00", "end": "16:00"},
    "New York": {"start": "13:00", "end": "22:00"},
}

def get_current_monday():
    """Calculate the date of the current week's Monday."""
    today = datetime.now()
    return today - timedelta(days=today.weekday())


def convert_to_24h(time_str):
    """Convert time from 12-hour (AM/PM) to 24-hour format."""
    try:
        time_obj = datetime.strptime(time_str, "%I:%M%p")
        return time_obj.strftime("%H:%M")
    except ValueError:
        return time_str


def get_trading_sessions(event_time):
    """Determine active trading sessions based on event time."""
    event_time_24h = convert_to_24h(event_time)
    event_time_obj = datetime.strptime(event_time_24h, "%H:%M").time()
    sessions = []

    for session, times in SESSIONS.items():
        start = datetime.strptime(times["start"], "%H:%M").time()
        end = datetime.strptime(times["end"], "%H:%M").time()

        if start > end:
            if event_time_obj >= start or event_time_obj < end:
                sessions.append(session)
        elif start <= event_time_obj < end:
            sessions.append(session)

    return sessions if sessions else ["After Hours"]


def convert_time_to_timezone(time_str, from_tz="UTC", to_tz="UTC"):
    """Convert event time from one timezone to another."""
    try:
        from_tz = pytz.timezone(from_tz)
        to_tz = pytz.timezone(to_tz)
    except pytz.exceptions.UnknownTimeZoneError as e:
        print(f"Invalid timezone: {e}")
        return time_str

    time_obj = datetime.strptime(convert_to_24h(time_str), "%H:%M")
    time_obj = from_tz.localize(time_obj)
    time_obj = time_obj.astimezone(to_tz)
    return time_obj.strftime("%H:%M")


def fetch_and_parse_xml(output_file, country_filter=None, title_filter=None, 
                       impact_filter=None, save_format="json", user_timezone=None):
    """Fetch and parse Forex Factory XML, applying filters and saving results."""
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch XML: {e}")
        return

    try:
        root = ET.fromstring(response.content)
    except ET.ParseError as e:
        print(f"Failed to parse XML: {e}")
        return

    all_events = []
    filtered_events = []

    for event in root.findall('event'):
        event_data = {
            'title': event.find('title').text,
            'country': event.find('country').text,
            'date': event.find('date').text,
            'time': event.find('time').text,
            'impact': event.find('impact').text,
            'forecast': event.find('forecast').text if event.find('forecast') is not None else None,
            'previous': event.find('previous').text if event.find('previous') is not None else None,
            'url': event.find('url').text,
        }
        event_data['sessions'] = get_trading_sessions(event_data['time'])

        if user_timezone:
            event_data['time'] = convert_time_to_timezone(event_data['time'], to_tz=user_timezone)

        all_events.append(event_data)

        if ((not country_filter or event_data['country'] == country_filter) and
            (not title_filter or title_filter.lower() in event_data['title'].lower()) and
            (not impact_filter or event_data['impact'] == impact_filter)):
            filtered_events.append(event_data)

    if save_format == "json":
        output_filename = f"{output_file}.json"
        with open(output_filename, 'w') as json_file:
            json.dump(filtered_events, json_file, indent=4)
        print(f"Filtered events saved to JSON file: {output_filename}")
    elif save_format == "txt":
        output_filename = f"{output_file}.txt"
        with open(output_filename, 'w') as txt_file:
            for event in filtered_events:
                event_str = (
                    f"Title: {event['title']}\n"
                    f"Country: {event['country']}\n"
                    f"Date: {event['date']}\n"
                    f"Time: {event['time']}\n"
                    f"Impact: {event['impact']}\n"
                    f"Forecast: {event['forecast']}\n"
                    f"Previous: {event['previous']}\n"
                    f"URL: {event['url']}\n"
                    f"Sessions: {', '.join(event['sessions'])}\n"
                    f"{'-' * 40}\n"
                )
                txt_file.write(event_str)
        print(f"Filtered events saved to TXT file: {output_filename}")


@click.command()
@click.option('--schedule', is_flag=True, help="Schedule the script to run every hour.")
@click.option('--country', type=str, help="Filter events by country (e.g., USD, EUR).")
@click.option('--title', type=str, help="Filter events by title (case-insensitive).")
@click.option('--impact', type=str, help="Filter events by impact (e.g., High, Medium, Low).")
@click.option('--save-format', type=click.Choice(['json', 'txt']), default="json", help="Save format: json or txt.")
@click.option('--output-file', type=str, default="filtered_events", help="Base name for the output file (without extension).")
@click.option('--timezone', type=str, default=None, help="Convert event times to the specified timezone (e.g., 'America/New_York').")
def main(schedule, country, title, impact, save_format, output_file, timezone):
    """Fetch and parse Forex Factory events with optional filters."""
    if schedule:
        print("Scheduling the script to run every hour...")
        fetch_and_parse_xml(output_file, country, title, impact, save_format, timezone)
        scheduler.every(1).hours.do(fetch_and_parse_xml, output_file, country, title, impact, save_format, timezone)
        while True:
            scheduler.run_pending()
            time.sleep(1)
    else:
        fetch_and_parse_xml(output_file, country, title, impact, save_format, timezone)


if __name__ == "__main__":
    main()