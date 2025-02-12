import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import schedule
import time

# URL of the XML forexFactory
URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"

def get_current_monday():
    today = datetime.now()
    # Calculate the date of the current Monday
    monday = today - timedelta(days=today.weekday())
    return monday

def fetch_and_parse_xml(formatted_monday):
    response = requests.get(URL)
    if response.status_code == 200:
        root = ET.fromstring(response.content)

        # Open files for writing
        with open(f'all_events_this_week_{formatted_monday}.txt', 'w') as all_file, open(f'high_impact_events_this_week_{formatted_monday}.txt', 'w') as high_file:
            for event in root.findall('event'):
                title = event.find('title').text
                country = event.find('country').text
                date = event.find('date').text
                time = event.find('time').text
                impact = event.find('impact').text
                forecast = event.find('forecast').text if event.find('forecast') is not None else None
                previous = event.find('previous').text if event.find('previous') is not None else None
                url = event.find('url').text
                
                # Create event string
                event_str = (
                    f"Title: {title}\n"
                    f"Country: {country}\n"
                    f"Date: {date}\n"
                    f"Time: {time}\n"
                    f"Impact: {impact}\n"
                    f"Forecast: {forecast}\n"
                    f"Previous: {previous}\n"
                    f"URL: {url}\n"
                    f"{'-' * 40}\n"
                )
                # Write to all events file
                all_file.write(event_str)
                
                # Write to high impact events file if impact is High
                if impact == 'High' and country == "USD":
                    high_file.write(event_str)
    else:
        print(f"Failed to fetch. Status code: {response.status_code}")
        return None
    
def main():
    # Calculate the current Monday's date
    current_monday = get_current_monday()
    formatted_monday = current_monday.strftime("%m-%d-%Y")
    fetch_and_parse_xml(formatted_monday)

# Schedule the main function to run every hour
schedule.every(1).hours.do(main)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
        