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

def main():
    args = parse_arguments()
    
    if args.interactive:
        print("🎶Interactive mode selected.🎶")
        print("Type notes like: C4 1")
        print("Type 'exit' to quit.")
    
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