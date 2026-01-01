import numpy as np
from scipy.io.wavfile import write
from engine.audio import (
    SAMPLE_RATE,
    generate_adsr_envelope,
)

def render_sequence_to_wav(
    note_events,
    output_path: str,
    amplitude: float = 0.5,
):
    """
    Render a sequence of notes to a wav file.
    """
    full_buffer = []
    
    for note, frequency, beats, seconds, in note_events:
        t = np.linspace(
            0,
            seconds,
            int(SAMPLE_RATE * seconds),
            endpoint=False,
        )
        
        wave = np.sin(2 * np.pi * frequency * t)
        
        envelope = generate_adsr_envelope(
            seconds,
            attack= 0.01,
            decay= 0.1,
            sustain_level= 0.7,
            release= 0.2,
            sample_rate= SAMPLE_RATE,
        )
        
        wave = amplitude *wave[:len(envelope)] * envelope
        
        full_buffer.append(wave)
        
        if not full_buffer:
            raise ValueError("No audio data to render.")
        
        audio = np.concatenate(full_buffer)
        
        #Normalize to int16
        audio /= np.max(np.abs(audio))
        audio_int16 = np.int16(audio * 32767)
        
        write(output_path, SAMPLE_RATE, audio_int16)