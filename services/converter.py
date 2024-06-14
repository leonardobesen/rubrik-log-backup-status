from datetime import datetime, timedelta
from typing import Optional
from configuration.configuration import get_timezone_info
import pytz


def iso_to_date(iso_str: Optional[str], correct_timezone=True) -> Optional[datetime]:
    timezone = get_timezone_info()

    if not iso_str:
        return None

    try:
        date_obj = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
        if correct_timezone:
            date_obj = date_obj.astimezone(pytz.timezone(timezone))
        return date_obj.replace(tzinfo=None)
    except ValueError:
        print(f"Invalid ISO8601 format provided")
        return None


def bytes_to_tb(bytes_size: int) -> float:
    return round(bytes_size/(1000**4), 2)


def seconds_to_duration(long_value: Optional[int]) -> Optional[timedelta]:
    if not long_value:
        return None

    try:
        time_delta = timedelta(seconds=long_value)
    except:
        return None

    return time_delta
