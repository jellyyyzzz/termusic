class TimingEngine:
    def __init__(self, bpm: float = 120.0):
        self.set_bpm(bpm)
    
    def set_bpm(self, bpm: float):
        if bpm <= 0 or bpm > 300:
            raise ValueError("BPM must be between 1 and 300.")
        self.bpm = bpm
        self.seconds_per_beat = 60.0 / bpm
    
    def beats_to_seconds(self, beats: float) -> float:
        return beats * self.seconds_per_beat