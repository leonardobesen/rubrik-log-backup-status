import datetime


def format_timedelta(td: datetime.timedelta) -> str:
    days = td.days
    hours, rem = divmod(td.seconds, 3600)
    minutes, _ = divmod(rem, 60)
    return f"{days}d {hours}h {minutes}m"
