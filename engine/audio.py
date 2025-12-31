import numpy as np
import sounddevice as sd

SAMPLE_RATE = 44100 #Standard sample rate for audio

def play_sine_wave(
    frequency: float,
    duration_seconds: float,
    amplitude: float = 0.5,
):
    """
    Play a sine wave at a given frequency and duratiion.
    """
    
    if frequency <= 0:
        return #No sound for non-positive frequencies
    
    if duration_seconds <= 0:
        return
    
    t = np.linspace(
        0,
        duration_seconds,
        int(SAMPLE_RATE * duration_seconds),
        endpoint=False,
    )
    
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    
    sd.play(wave, SAMPLE_RATE)
    sd.wait() #Wait until sound has finished playing