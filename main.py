#!/usr/bin/env python3
"""Find an HLS playlist when needed, then download the video as MP4."""

import argparse
from pathlib import Path
from urllib.parse import urlsplit

from download_video import download_video
from find_hls import find_hls_url


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="video page or direct media URL")
    parser.add_argument(
        "-o", "--output-dir", type=Path, default=Path("downloads"),
        help="destination directory (default: ./downloads)",
    )
    parser.add_argument("--referer", help="override the page URL sent as Referer")
    parser.add_argument("--timeout", type=int, default=30, help="seconds to watch for HLS (default: 30)")
    parser.add_argument("--headless", action="store_true", help="hide Chrome during HLS discovery")
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be positive")

    parsed = urlsplit(args.url)
    host = parsed.hostname or ""
    is_youtube = host in {"youtube.com", "youtu.be"} or host.endswith(".youtube.com")
    is_media = Path(parsed.path).suffix.lower() in {".m3u8", ".mpd", ".mp4", ".webm", ".mov", ".m4v"}
    url, referer = args.url, args.referer
    if not is_youtube and not is_media:
        print("Opening Chrome to find an HLS playlist. Press Play in the browser if needed.")
        found = find_hls_url(args.url, args.timeout, args.headless)
        # print('url: ', found)
        # exit(0)
        if found:
            url = found
            referer = referer or args.url
            print("Found an HLS playlist; downloading it.")
        else:
            print("No HLS playlist found; trying the page URL directly.")

    try:
        return download_video(url, args.output_dir, referer)
    except FileNotFoundError as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
