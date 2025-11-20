import schedule
import time
from plyer import notification
from data_manager import get_upcoming_events, load_routines
from datetime import datetime, timedelta

def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="Timetable App",
        timeout=10
    )

def check_upcoming():
    try:
        now = datetime.now()
        today_str = now.strftime('%Y-%m-%d')
        today_weekday = now.strftime('%A')

        # Check lessons/exams
        upcoming = get_upcoming_events()
        for _, event in upcoming.iterrows():
            event_dt = datetime.strptime(f"{event['Date']} {event['Start_Time']}", '%Y-%m-%d %H:%M')
            if timedelta(minutes=0) < event_dt - now <= timedelta(minutes=1440):
                send_notification("Upcoming Event", f"{event['Name']} starts at {event['Start_Time']} on {event['Date']}")

        # Check today's routines
        routines_df = load_routines()
        today_routines = routines_df[(routines_df['Day_of_Week'] == today_weekday) | (routines_df['Day_of_Week'] == 'Everyday')]
        for _, routine in today_routines.iterrows():
            routine_dt = datetime.strptime(f"{today_str} {routine['Start_Time']}", '%Y-%m-%d %H:%M')
            if timedelta(minutes=0) < routine_dt - now <= timedelta(minutes=1440):
                send_notification("Routine Reminder", f"{routine['Name']} starts at {routine['Start_Time']} today")
    except Exception as e:
        print(f"Reminder error: {e}")  # Log errors without crashing

def check_reminders():
    schedule.every(10).minutes.do(check_upcoming)  # Or every(1).minutes for testing
    while True:
        schedule.run_pending()
        time.sleep(1)