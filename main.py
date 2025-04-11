#!/usr/bin/env python3

import subprocess
import os
from datetime import datetime
from pathlib import Path

RECORD_INTERVAL = 180
MAX_FILES = 3
OUTPUT_DIR = Path.home() / "screen_records"
OUTPUT_DIR.mkdir(exist_ok=True)


def cleanup_old_files():
    files = sorted(OUTPUT_DIR.glob("*.mp4"), key=os.path.getmtime)
    while len(files) >= MAX_FILES:
        files.pop(0).unlink()


def record_screen():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = OUTPUT_DIR / f"{timestamp}.mp4"

    ffmpeg_cmd = [
        "ffmpeg",
        "-video_size", "1280x720",
        "-framerate", "15",
        "-f", "x11grab",
        "-i", ":0.0",
        "-vf", "format=gray",
        "-preset", "ultrafast",
        "-t", str(RECORD_INTERVAL),
        "-y",
        str(output_file)
    ]

    subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    while True:
        cleanup_old_files()
        record_screen()


if __name__ == "__main__":
    main()
