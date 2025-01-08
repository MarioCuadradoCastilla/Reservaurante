from datetime import datetime, timedelta

def parse_date_time(date_str, time_str):
    """Convert date and time strings to datetime object"""
    datetime_str = f"{date_str} {time_str}"
    return datetime.strptime(datetime_str, '%d/%m/%Y %H:%M')

def get_alternative_times(current_time, hours_range=3):
    """Generate a range of times around the given time"""
    times = []
    for hour_offset in range(-hours_range, hours_range + 1):
        alternative_time = current_time + timedelta(hours=hour_offset)
        if 8 <= alternative_time.hour <= 22:  # Business hours
            times.append(alternative_time)
    return times

def format_time(datetime_obj):
    """Format datetime object to time string"""
    return datetime_obj.strftime("%H:%M")