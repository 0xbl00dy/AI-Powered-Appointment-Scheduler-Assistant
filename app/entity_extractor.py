import re


def extract_entities(text: str):
    date_pattern = r"(next\s+\w+|this\s+\w+|\b\d{1,2}/\d{1,2}/\d{4}\b)"
    time_pattern = r"(\d{1,2}(:\d{2})?\s?(am|pm))"
    dept_pattern = r"(dentist|doctor|cardiology|orthopedic)"

    date = re.search(date_pattern, text, re.IGNORECASE)
    time = re.search(time_pattern, text, re.IGNORECASE)
    dept = re.search(dept_pattern, text, re.IGNORECASE)

    entities = {
        "date_phrase": date.group(0) if date else None,
        "time_phrase": time.group(0) if time else None,
        "department": dept.group(0) if dept else None,
    }

    confidence = 0.85 if all(entities.values()) else 0.60

    return entities, confidence
