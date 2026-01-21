from datetime import datetime
from dateparser.search import search_dates


def normalize_date_time(date_phrase: str, time_phrase: str):
    if not date_phrase or not time_phrase:
        return None, 0.0

    combined = f"{date_phrase} {time_phrase}"

    results = search_dates(
        combined,
        settings={
            "RELATIVE_BASE": datetime.now(),
            "PREFER_DATES_FROM": "future",
            "TIMEZONE": "Asia/Kolkata",
            "RETURN_AS_TIMEZONE_AWARE": False,
        },
    )

    if not results:
        return None, 0.0

    # Take the first detected date
    _, parsed_date = results[0]

    normalized = {
        "date": parsed_date.strftime("%Y-%m-%d"),
        "time": parsed_date.strftime("%H:%M"),
        "tz": "Asia/Kolkata",
    }

    return normalized, 0.90