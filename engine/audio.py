import numpy as np
import sounddevice as sd

SAMPLE_RATE = 44100 #Standard sample rate for audio

def exponential_curve(length: int, start: float, end: float):
    """
    Generate an exponential curve from start to end.
    """
    if length <= 0:
        return np.array([])
    
    curve = np.logspace(0, 1, length, endpoint=False)
    curve = curve / curve.max() #Normalize to 0-1
    
    return start + (end - start) * curve

def generate_adsr_envelope(
    duration_seconds: float,
    attack: float,
    decay: float,
    sustain_level: float,
    release: float,
    sample_rate: int,
):
    """
    Generate a linear ADSR envelope.
    """
    total_samples = int(duration_seconds * sample_rate)
    
    attack_samples = int(attack * sample_rate)
    decay_samples = int(decay * sample_rate)
    release_samples = int(release * sample_rate)
    
    sustain_samples = total_samples - (
        attack_samples + decay_samples + release_samples
    )
    
    if sustain_samples < 0:
        raise ValueError("ADSR time exceed note duration.")
    
    #Attack: linear(0 -> 1)
    attack_env = np.linspace(0, 1, attack_samples, endpoint=False)
    
    #Decay: exponential(1 -> sustain_level)
    decay_env = exponential_curve(
        decay_samples, start = 1.0, end = sustain_level
    )
    
    #Sustain: constant
    sustain_env = np.full(sustain_samples, sustain_level)
    
    #Release: exponential(sustain level -> 0)
    release_env = exponential_curve(
        release_samples, start = sustain_level, end = 0.0
    )
    
    envelope = np.concatenate(
        (attack_env, decay_env, sustain_env, release_env)
    )
    return envelope

def sine_wave(frequency, t):
    return np.sin(2 * np.pi * frequency * t)

def square_wave(frequency, t):
    return np.sign(np.sin(2 * np.pi * frequency * t))

def saw_wave(frequency, t):
    return 2 * (t * frequency - np.floor(0.5 + t * frequency))

def play_wave(
    frequency: float,
    duration_seconds: float,
    waveform: str = "sine",
    amplitude: float = 0.5,
):
    """
    Play a sine wave at a given frequency and duratiion.
    """
    
    if frequency <= 0 or duration_seconds <=0:
        return #No sound for non-positive frequencies
    
    t = np.linspace(
        0,
        duration_seconds,
        int(SAMPLE_RATE * duration_seconds),
        endpoint=False,
    )
    
    if waveform == "sine":
        wave = sine_wave(frequency, t)
    elif waveform == "square":
        wave = square_wave(frequency, t)
    elif waveform == "saw":
        wave = saw_wave(frequency, t)
    else:
        raise ValueError(f"Unknown waveform: {waveform}")
    
    #ADSR parameters
    attack = 0.01
    decay = 0.1
    sustain = 0.7
    release = 0.2
    
    envelope = generate_adsr_envelope(
        duration_seconds,
        attack,
        decay,
        sustain,
        release,
        SAMPLE_RATE,
    )
    
    wave = amplitude * wave[:len(envelope)] * envelope
    
    sd.play(wave, SAMPLE_RATE)
    sd.wait() #Wait until sound has finished playing