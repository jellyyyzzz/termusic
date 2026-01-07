import time
from engine.audio import play_wave

def play_sequence(note_events, waveform="sine"):
    """
    Play a list of notes sequentially.
    
    note_events format:
    [
        (note, frequency, beats, seconds),
        ...
    ]
    """
    for note, frequency, beats, seconds, wf in note_events:
        play_wave(frequency, seconds, wf)
        time.sleep(0.1) #Tiny gap to avoid edge overlap