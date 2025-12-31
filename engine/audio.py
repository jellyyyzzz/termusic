import numpy as np
import sounddevice as sd

SAMPLE_RATE = 44100 #Standard sample rate for audio

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
    
    #Attack: 0 -> 1
    attack_env = np.linspace(0, 1, attack_samples, endpoint=False)
    
    #Decay: 1 -> sustain_level
    decay_env = np.linspace(1, sustain_level, decay_samples, endpoint=False)
    
    #Sustain: constant
    sustain_env = np.full(sustain_samples, sustain_level)
    
    #Release: sustain level -> 0
    release_env = np.linspace(
        sustain_level, 0, release_samples, endpoint=False
    )
    
    envelope = np.concatenate(
        (attack_env, decay_env, sustain_env, release_env)
    )
    return envelope

def play_sine_wave(
    frequency: float,
    duration_seconds: float,
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
    
    wave = np.sin(2 * np.pi * frequency * t)
    
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