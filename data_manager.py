# timetable_app/data_manager.py

import pandas as pd
from datetime import datetime, timedelta
import os

LESSONS_FILE = 'lessons_exams.csv'
ROUTINES_FILE = 'daily_routines.csv'

def initialize_files():
    if not os.path.exists(LESSONS_FILE):
        pd.DataFrame(columns=['Type', 'Name', 'Date', 'Start_Time', 'End_Time', 'Day_of_Week', 'Location', 'Notes']).to_csv(LESSONS_FILE, index=False)
    if not os.path.exists(ROUTINES_FILE):
        pd.DataFrame(columns=['Name', 'Start_Time', 'End_Time', 'Day_of_Week', 'Notes']).to_csv(ROUTINES_FILE, index=False)

def load_lessons():
    try:
        return pd.read_csv(LESSONS_FILE)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=['Type', 'Name', 'Date', 'Start_Time', 'End_Time', 'Day_of_Week', 'Location', 'Notes'])

def load_routines():
    try:
        return pd.read_csv(ROUTINES_FILE)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=['Name', 'Start_Time', 'End_Time', 'Day_of_Week', 'Notes'])

def save_lessons(df):
    df.to_csv(LESSONS_FILE, index=False)

def save_routines(df):
    df.to_csv(ROUTINES_FILE, index=False)

def add_lesson_exam(entry_type, name, date, start_time, end_time, location, notes):
    day_of_week = datetime.strptime(date, '%Y-%m-%d').strftime('%A')
    df = load_lessons()
    new_entry = pd.DataFrame({
        'Type': [entry_type.capitalize()],
        'Name': [name],
        'Date': [date],
        'Start_Time': [start_time],
        'End_Time': [end_time],
        'Day_of_Week': [day_of_week],
        'Location': [location],
        'Notes': [notes]
    })
    df = pd.concat([df, new_entry], ignore_index=True)
    save_lessons(df)

def add_routine(name, start_time, end_time, day_of_week, notes):
    df = load_routines()
    new_entry = pd.DataFrame({
        'Name': [name],
        'Start_Time': [start_time],
        'End_Time': [end_time],
        'Day_of_Week': [day_of_week],
        'Notes': [notes]
    })
    df = pd.concat([df, new_entry], ignore_index=True)
    save_routines(df)

def edit_lesson_exam(index, updates):
    df = load_lessons()
    for key, value in updates.items():
        df.at[index, key] = value
    if 'Date' in updates:
        df.at[index, 'Day_of_Week'] = datetime.strptime(updates['Date'], '%Y-%m-%d').strftime('%A')
    save_lessons(df)

def edit_routine(index, updates):
    df = load_routines()
    for key, value in updates.items():
        df.at[index, key] = value
    save_routines(df)

def delete_lesson_exam(index):
    df = load_lessons()
    df = df.drop(index).reset_index(drop=True)
    save_lessons(df)

def delete_routine(index):
    df = load_routines()
    df = df.drop(index).reset_index(drop=True)
    save_routines(df)

def get_daily_schedule(date):
    day_of_week = datetime.strptime(date, '%Y-%m-%d').strftime('%A')
    lessons_df = load_lessons()
    routines_df = load_routines()
    daily_lessons = lessons_df[lessons_df['Date'] == date]
    daily_routines = routines_df[(routines_df['Day_of_Week'] == day_of_week) | (routines_df['Day_of_Week'] == 'Everyday')]
    return daily_lessons, daily_routines

def get_weekly_schedule(start_date):
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    weekly_data = {}
    for i in range(7):
        day = (start_dt + timedelta(days=i)).strftime('%Y-%m-%d')
        weekly_data[day] = get_daily_schedule(day)
    return weekly_data

def get_semester_schedule():
    return load_lessons().sort_values('Date'), load_routines()

def get_upcoming_events():
    today = datetime.now().strftime('%Y-%m-%d')
    lessons_df = load_lessons()
    upcoming = lessons_df[lessons_df['Date'] >= today].sort_values('Date').head(5)
    return upcoming

def check_conflicts(date):
    lessons_df = load_lessons()
    daily = lessons_df[lessons_df['Date'] == date].copy()
    if daily.empty:
        return []
    daily['Start'] = pd.to_datetime(daily['Date'] + ' ' + daily['Start_Time'])
    daily['End'] = pd.to_datetime(daily['Date'] + ' ' + daily['End_Time'])
    daily = daily.sort_values('Start')
    conflicts = []
    for i in range(1, len(daily)):
        if daily.iloc[i]['Start'] < daily.iloc[i-1]['End']:
            conflicts.append(f"Conflict between {daily.iloc[i-1]['Name']} and {daily.iloc[i]['Name']}")
    return conflicts