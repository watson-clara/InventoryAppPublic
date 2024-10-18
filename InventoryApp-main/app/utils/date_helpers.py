from datetime import datetime

def format_date(date):
    return date.strftime('%Y-%m-%d %H:%M:%S')

def is_date_within_range(date, start_date, end_date):
    return start_date <= date <= end_date

