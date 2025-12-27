import re

NOTE_PATTERN = re.compile(r"^[A-G](#)?[0-8]$")

def is_valid_note(note: str) -> bool:
    return bool(NOTE_PATTERN.match(note))

def is_valid_duration(value: str) -> bool:
    try:
        duration = float(value)
        return duration > 0
    except ValueError:
        return False