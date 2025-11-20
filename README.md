# Timetable App

## Overview
This is a GUI-based timetable application built with Python and Tkinter. It allows managing lessons, exams, and daily routines, viewing schedules, editing/deleting entries, checking conflicts, and receiving reminders.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python main.py`

## Features
- **Add Entries**: Add lessons, exams, or routines via the GUI form.
- **View Schedules**: Daily, weekly, semester, or upcoming views.
- **Edit/Delete**: Select and modify or remove entries.
- **Check Conflicts**: Detect time overlaps for a specific date.
- **Reminders**: Desktop notifications for upcoming events (checks every 10 minutes).

## Data Storage
Data is stored in `lessons_exams.csv` and `daily_routines.csv`. These are auto-created if missing.

## Troubleshooting
- Ensure Python 3.x is installed.
- If notifications don't work, check plyer compatibility with your OS.
- For calendar issues, verify tkcalendar installation.

## Expansion Ideas
- Integrate Google Calendar API for sync.
- Add export to iCal.
- Enhance GUI with themes or drag-and-drop.