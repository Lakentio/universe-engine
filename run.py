#!/usr/bin/env python3

import sys
import os
import argparse

# Add the 'src' directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def _parse_args():
    parser = argparse.ArgumentParser(description="Universe Engine launcher")
    parser.add_argument('--load', '-l', help='Load save by name or filename')
    parser.add_argument('--save', '-s', help='Save on start with given name')
    parser.add_argument('--fps', type=int, help='Override target FPS')
    parser.add_argument('--profile', action='store_true', help='Enable basic profiling/logging')
    parser.add_argument("--version", action="version", version="Universe Engine " + __import__('src').version)
    parser.add_argument("--dev", action="store_true", help="open the developer page on GitHub")
    return parser.parse_args()

if __name__ == "__main__":
    args = _parse_args()
    
    if args.dev:
        print("visit the dev page in -> https://github.com/Lakentio")

    from src.main import main

    main(load=args.load, save_on_start=args.save, fps=args.fps, profile=args.profile)