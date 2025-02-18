import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import schedule
import time
import click
import json

# URL of the XML forexFactory
URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"

def get_current_monday():
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    return monday

def fetch_and_parse_xml(output_file, country_filter=None, title_filter=None, impact_filter=None, save_format="json"):
    response = requests.get(URL)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
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
                'url': event.find('url').text
            }
            all_events.append(event_data)

            # Apply filters
            if (not country_filter or event_data['country'] == country_filter) and \
               (not title_filter or title_filter.lower() in event_data['title'].lower()) and \
               (not impact_filter or event_data['impact'] == impact_filter):
                filtered_events.append(event_data)

        # Save to file
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
                        f"{'-' * 40}\n"
                    )
                    txt_file.write(event_str)
            print(f"Filtered events saved to TXT file: {output_filename}")
    else:
        print(f"Failed to fetch. Status code: {response.status_code}")

def run_scheduled_task(output_file, country_filter=None, title_filter=None, impact_filter=None, save_format="json"):
    fetch_and_parse_xml(output_file, country_filter, title_filter, impact_filter, save_format)

@click.command()
@click.option('--schedule', is_flag=True, help="Schedule the script to run every hour.")
@click.option('--country', type=str, help="Filter events by country (e.g., USD, EUR).")
@click.option('--title', type=str, help="Filter events by title (case-insensitive).")
@click.option('--impact', type=str, help="Filter events by impact (e.g., High, Medium, Low).")
@click.option('--save-format', type=click.Choice(['json', 'txt']), default="json", help="Save format: json or txt.")
@click.option('--output-file', type=str, default="filtered_events", help="Base name for the output file (without extension).")
def main(schedule, country, title, impact, save_format, output_file):
    """Fetch and parse Forex Factory events with filters for country, title, and impact."""
    if schedule:
        print("Scheduling the script to run every hour...")
        schedule.every(1).hours.do(run_scheduled_task, output_file, country, title, impact, save_format)
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        print("Running the script once...")
        run_scheduled_task(output_file, country, title, impact, save_format)

if __name__ == "__main__":
    main()