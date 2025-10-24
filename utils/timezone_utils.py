"""
Timezone utilities for Carely application
All times are in Central Time (America/Chicago) with automatic DST handling
"""

from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo
from typing import Optional

# Central Time Zone (handles CST/CDT automatically)
CENTRAL_TZ = ZoneInfo("America/Chicago")


def now_central() -> datetime:
    """
    Get current datetime in Central Time
    
    Returns:
        Timezone-aware datetime in Central Time
    """
    return datetime.now(CENTRAL_TZ)


def to_central(dt: datetime) -> datetime:
    """
    Convert any datetime to Central Time
    
    Args:
        dt: Datetime object (naive or aware)
    
    Returns:
        Timezone-aware datetime in Central Time
    """
    if dt.tzinfo is None:
        # Assume naive datetimes are UTC
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))
    return dt.astimezone(CENTRAL_TZ)


def make_aware_central(dt: datetime) -> datetime:
    """
    Make a naive datetime timezone-aware in Central Time
    
    Args:
        dt: Naive datetime object
    
    Returns:
        Timezone-aware datetime in Central Time
    """
    if dt.tzinfo is not None:
        return to_central(dt)
    return dt.replace(tzinfo=CENTRAL_TZ)


def combine_date_time_central(date: datetime, time_obj: time) -> datetime:
    """
    Combine a date and time into a timezone-aware Central Time datetime
    
    Args:
        date: Date object or datetime
        time_obj: Time object
    
    Returns:
        Timezone-aware datetime in Central Time
    """
    if isinstance(date, datetime):
        date = date.date()
    
    dt = datetime.combine(date, time_obj)
    return make_aware_central(dt)


def parse_time_central(time_str: str) -> time:
    """
    Parse time string (HH:MM format) to time object
    
    Args:
        time_str: Time string in "HH:MM" format
    
    Returns:
        Time object
    """
    hour, minute = map(int, time_str.split(':'))
    return time(hour=hour, minute=minute)


def create_central_datetime(
    year: int,
    month: int,
    day: int,
    hour: int = 0,
    minute: int = 0,
    second: int = 0
) -> datetime:
    """
    Create a timezone-aware datetime in Central Time
    
    Args:
        year: Year
        month: Month (1-12)
        day: Day of month
        hour: Hour (0-23)
        minute: Minute (0-59)
        second: Second (0-59)
    
    Returns:
        Timezone-aware datetime in Central Time
    """
    return datetime(year, month, day, hour, minute, second, tzinfo=CENTRAL_TZ)


def format_central_time(dt: datetime, format_str: str = "%Y-%m-%d %I:%M %p %Z") -> str:
    """
    Format datetime in Central Time for display
    
    Args:
        dt: Datetime object
        format_str: strftime format string (default includes timezone)
    
    Returns:
        Formatted datetime string in Central Time
    """
    central_dt = to_central(dt)
    return central_dt.strftime(format_str)


def start_of_day_central(dt: Optional[datetime] = None) -> datetime:
    """
    Get start of day (midnight) in Central Time
    
    Args:
        dt: Datetime object (defaults to now)
    
    Returns:
        Timezone-aware datetime at start of day in Central Time
    """
    if dt is None:
        dt = now_central()
    else:
        dt = to_central(dt)
    
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def end_of_day_central(dt: Optional[datetime] = None) -> datetime:
    """
    Get end of day (23:59:59) in Central Time
    
    Args:
        dt: Datetime object (defaults to now)
    
    Returns:
        Timezone-aware datetime at end of day in Central Time
    """
    if dt is None:
        dt = now_central()
    else:
        dt = to_central(dt)
    
    return dt.replace(hour=23, minute=59, second=59, microsecond=999999)


def get_next_occurrence(time_obj: time, start_from: Optional[datetime] = None) -> datetime:
    """
    Get next occurrence of a specific time in Central Time
    
    Args:
        time_obj: Time to find next occurrence of
        start_from: Start searching from this datetime (defaults to now)
    
    Returns:
        Next occurrence of the time in Central Time
    """
    if start_from is None:
        start_from = now_central()
    else:
        start_from = to_central(start_from)
    
    # Combine with today's date
    next_time = datetime.combine(start_from.date(), time_obj, tzinfo=CENTRAL_TZ)
    
    # If already passed today, use tomorrow
    if next_time <= start_from:
        next_time = next_time + timedelta(days=1)
    
    return next_time


def is_dst_central(dt: Optional[datetime] = None) -> bool:
    """
    Check if given datetime is in Daylight Saving Time (CDT) in Central Time
    
    Args:
        dt: Datetime to check (defaults to now)
    
    Returns:
        True if in DST (CDT), False if in standard time (CST)
    """
    if dt is None:
        dt = now_central()
    else:
        dt = to_central(dt)
    
    return dt.dst() != timedelta(0)


def get_timezone_name(dt: Optional[datetime] = None) -> str:
    """
    Get timezone abbreviation (CST or CDT) for given datetime
    
    Args:
        dt: Datetime to check (defaults to now)
    
    Returns:
        Timezone abbreviation ("CST" or "CDT")
    """
    if dt is None:
        dt = now_central()
    else:
        dt = to_central(dt)
    
    return dt.strftime("%Z")
