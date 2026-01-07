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

def is_tempo_command(line: str) -> bool:
    return line.lower().startswith("@tempo")

def parse_tempo(line: str) -> float:
    parts = line.split()
    if len(parts) != 2:
        raise ValueError("Invalid tempo command format.")
    
    bpm = float(parts[1])
    if bpm <= 0 or bpm > 300:
        raise ValueError("BPM out of allowed range.")
    
    return bpm

def is_synth_command(line: str) -> bool:
    return line.lower().startswith("@synth")

def parse_synth(line: str) -> str:
    parts = line.split()
    if len(parts) != 2:
        raise ValueError("Invalid synth command.")
    
    synth = parts[1].lower()
    if synth not in ["sine", "square", "saw"]:
        raise ValueError("Unsupported synth type.")
    return synth