#!/usr/bin/env python3
"""Download a video page or direct media URL with audio as an MP4 file."""

import argparse
import shutil
from pathlib import Path

from yt_dlp import YoutubeDL


def download_video(url, output_dir=Path("downloads"), referer=None):
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise FileNotFoundError("ffmpeg and ffprobe must be installed and available on PATH")

    output_dir.mkdir(parents=True, exist_ok=True)
    options = {
        "format": "bv[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/bv+ba/b",
        "merge_output_format": "mp4/mkv",
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": str(output_dir / "%(title).200B [%(id)s].%(ext)s"),
        "noplaylist": True,
    }
    if referer:
        options["http_headers"] = {"Referer": referer}
    with YoutubeDL(options) as downloader:
        return downloader.download([url])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="URL of the video to download")
    parser.add_argument(
        "-o", "--output-dir", type=Path, default=Path("downloads"),
        help="destination directory (default: ./downloads)",
    )
    parser.add_argument("--referer", help="page URL required by some media hosts")
    args = parser.parse_args()

    try:
        return download_video(args.url, args.output_dir, args.referer)
    except FileNotFoundError as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
