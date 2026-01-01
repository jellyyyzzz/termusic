import time
from engine.audio import play_sine_wave

def play_sequence(note_events):
    """
    Play a list of notes sequentially.
    
    note_events format:
    [
        (note, frequency, beats, seconds),
        ...
    ]
    """
    for note, frequency, beats, seconds, in note_events:
        play_sine_wave(frequency, seconds)
        time.sleep(0.1) #Tiny gap to avoid edge overlap