import argparse
import sys

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
            
            note, duration = parts
            
            #Store raw input safely (no execution)
            collected_lines.append((note, duration))
            print(f"✅ Captured: note = {note}, duration = {duration}")
        
        except KeyboardInterrupt:
            print("\n🛑 Interupted by user.")
            break
        
        print("\n✅ Session summary: ")
        for n, d in collected_lines:
            print(f" - {n} for {d} breat(s)")
            
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