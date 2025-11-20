import schedule
import time
from plyer import notification
from data_manager import get_upcoming_events
from datetime import datetime, timedelta

def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="Timetable App",
        timeout=10
    )

def check_upcoming():
    upcoming = get_upcoming_events()
    now = datetime.now()
    for _, event in upcoming.iterrows():
        event_dt = datetime.strptime(f"{event['Date']} {event['Start_Time']}", '%Y-%m-%d %H:%M')
        if timedelta(minutes=0) < event_dt - now < timedelta(minutes=30):  # Remind 30 min before
            send_notification("Upcoming Event", f"{event['Name']} starts at {event['Start_Time']} on {event['Date']}")

def check_reminders():
    schedule.every(10).minutes.do(check_upcoming)  # Check every 10 minutes
    while True:
        schedule.run_pending()
        time.sleep(1)