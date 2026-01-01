import argparse
import sys
from engine.timing import TimingEngine
from parser.syntax import (
    is_valid_note,
    is_valid_duration,
    is_tempo_command,
    parse_tempo
)
from engine.frequency import note_to_frequency
from engine.audio import play_sine_wave
from engine.sequencer import play_sequence

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Termusic - A terminal-based music creation engine"
    )
    
    mode = parser.add_mutually_exclusive_group(required=True)
    
    mode.add_argument(
        "--interactive",
        action="store_true",
        help="Store interactive music input mode"
    )
    
    mode.add_argument(
        "--play",
        type=str,
        metavar="FILE",
        help="Play a music score file"
    )
    
    mode.add_argument(
        "--export",
        type=str,
        metavar="OUTPUT",
        help="Export audio to a WAV file"
    )
    
    return parser.parse_args()


timing = TimingEngine(bpm = 120.0)
def interactive_loop():
    print("🎶Interactive mode selected.🎶")
    print("Type notes like: C4 1")
    print("Type 'exit' to quit.\n")
    
    collected_lines = []
    
    while True:
        try:
            user_input = input("> ").strip()
            
            #Empty input protection
            if not user_input:
                print("⚠️No input detected.")
                continue
            
            #Exit condition
            if user_input.lower() == "exit":
                print("👋Exiting interactive mode.")
                break
            
            #Temporary validation
            parts = user_input.split()  
            if len(parts) != 2:
                print("❌Invalid format. Use: NOTE DURATION (e.g., C4 1)")
                continue
            
            if is_tempo_command(user_input):
                try:
                    new_bpm = parse_tempo(user_input)
                    timing.set_bpm(new_bpm)
                    print(f"🎼 Tempo set to {new_bpm} BPM")
                except ValueError as e:
                    print(f"❌ {e}")
                continue
            
            note, duration = parts
            
            if not is_valid_note(note):
                print(f"❌ Invalid note: {note}")
                continue
            
            if not is_valid_duration(duration):
                print(f"❌ Invalid duration: {duration}")
                continue
            
            frequency = note_to_frequency(note)
            seconds =  timing.beats_to_seconds(float(duration))
            
            collected_lines.append(
                (note, frequency, float(duration), seconds)
            )
            
            print(
                f"✅ Captured: {note} | {frequency} Hz | "
                f"{duration} beat(s) | {seconds:.3f} sec"
            )
            
            """if collected_lines:
                print("\n▶️ Playing sequence...\n")
                play_sequence(collected_lines)"""
            
        except KeyboardInterrupt:
            print("\n🛑 Interupted by user.")
            break
        
        print("\n✅ Session summary: ")
        for note, freq, beats, seconds in collected_lines:
            print(
                f" - {note} | {freq} Hz | {beats} beat(s) | {seconds:.3f} sec"
            )
        
        if collected_lines:
            print("\n▶️ Playing sequence...\n")
            play_sequence(collected_lines)
            
def main():
    args = parse_arguments()
    
    if args.interactive:
        interactive_loop()
    
    if args.play:
        print(f"📜Playing score file: {args.play}")
    
    if args.export:
        print(f"export enabled -> {args.export}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑Interupted by user.")
        sys.exit(0)