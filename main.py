import subprocess
import os
from datetime import datetime
from pathlib import Path

RECORD_INTERVAL = 180
MAX_FILES = 3
OUTPUT_DIR = Path.home() / "screen_records"
OUTPUT_DIR.mkdir(exist_ok=True)


def get_screen_resolution() -> str | None:
    try:
        output = subprocess.check_output(["xdpyinfo"]).decode()
        for line in output.splitlines():
            if "dimensions:" in line:
                return line.split()[1]
    except Exception:
        return "1920x1080"


def cleanup_old_files():
    files = sorted(OUTPUT_DIR.glob("*.mp4"), key=os.path.getmtime)
    while len(files) >= MAX_FILES:
        files.pop(0).unlink()


def record_screen():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = OUTPUT_DIR / f"{timestamp}.mp4"
    display = os.getenv("DISPLAY", ":0")
    resolution = get_screen_resolution()

    ffmpeg_cmd = [
        "ffmpeg",
        "-video_size", resolution,
        "-framerate", "15",
        "-f", "x11grab",
        "-i", display,
        "-vf", "scale=1280:720,format=gray",
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
