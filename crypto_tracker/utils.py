# crypto_tracker/utils.py

from datetime import datetime, timedelta

def is_within_X_minutes(date: datetime, minutes_delta:int) -> bool:
    """
    Checks if the given date is earlier than X minutes ago from now.
    """
    now = datetime.now()  # Get the current time
    X_minutes_ago = now - timedelta(minutes=minutes_delta)  
    return date > X_minutes_ago  # Return True if the date is earlier than X minutes ago

def to_datetime(timestamp_millis: str) -> datetime:
    """
    Converts the timestamp which is in milliseconds to datetime, used in Binance API Client
    """
    return datetime.fromtimestamp(int(timestamp_millis / 1000))

def to_timestamp_millis(date: datetime) -> int:
    """
    Converts the datetime to timestamp in miliseconds, used in Binance API Client
    """
    return int(datetime.timestamp(date) * 1000)

def validate_arguments(args: dict, required_args: list):
    """Validate required arguments."""
    missing_args = [arg for arg in required_args if not args.get(arg)]
    if missing_args:
        raise ValueError(f"Missing required arguments: {', '.join(missing_args)}")
