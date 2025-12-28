import math

NOTE_OFFSETS = {
    "C": -9,
    "C#": -8,
    "D": -7,
    "D#": -6,
    "E": -5,
    "F": -4,
    "F#": -3,
    "G": -2,
    "G#": -1,
    "A": 0,
    "A#": 1,
    "B": 2,
}

def note_to_frequency(note: str) -> float:
    """
    Convert a note like C4 or D#5 to frequency in Hz.
    """
    if len(note) == 2:
        name = note[0]
        octave = int(note[1])
    else:
        name = note[:2]
        octave = int(note[2])
    
    semitone_offset = NOTE_OFFSETS[name]
    octave_offset = (octave - 4) * 12
    total_semitones = semitone_offset + octave_offset
    
    frequency = 440.0 * (2** (total_semitones / 12))
    return round(frequency, 2)