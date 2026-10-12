# Video downloader

Download a video page, direct `.m3u8` HLS playlist, YouTube URL, or direct media URL with its audio and save the result as an MP4 file. The `main.py` script uses Chrome to find HLS requests on video pages, then [yt-dlp](https://github.com/yt-dlp/yt-dlp) and [FFmpeg](https://ffmpeg.org/) to download and combine the streams.

## Setup

Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or another Conda distribution, then run from this folder:

```sh
conda env create -f environment.yml
conda activate video-download
```

If you already created the environment, run `conda env update -n video-download -f environment.yml` instead. The environment includes Python 3.11, `yt-dlp[default]`, Playwright, FFmpeg and FFprobe, and Deno for YouTube support. Install [Google Chrome](https://www.google.com/chrome/) for HLS discovery. Check the media tools with `ffmpeg -version` and `ffprobe -version`.

## Use

```sh
python main.py "https://example.com/watch/123"
python main.py "https://example.com/watch/123" --timeout 60 --output-dir ~/Videos
python main.py "https://media.example.com/video/master.m3u8"
python main.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

For a video page, Chrome opens and watches network responses for up to 30 seconds. Press Play in that browser window if the video does not start automatically. When an HLS playlist appears, `main.py` passes its URL to the downloader and uses the page URL as the Referer. If none appears, it tries the page URL directly with yt-dlp. YouTube and direct media URLs skip Chrome. Use `--headless` only when playback starts without interaction; use `--referer PAGE_URL` to override the Referer.

By default, the MP4 is saved under `./downloads/` with the video title and ID in its filename. The script downloads one video per invocation, even if the page URL belongs to a playlist. It prefers MP4 video plus M4A audio; when those are unavailable, it tries other available video/audio formats or a combined stream, then converts the result to MP4 if needed. Conversion may take time and can reduce quality. To skip browser discovery for any URL, run `python download_video.py URL` directly.

Discovery only sees HLS requests made while Chrome is open. Chrome uses a temporary profile, so your usual Chrome cookies and extensions are not available. Some sites require a login, cookies, or other headers to download a discovered URL; DRM-protected videos are not supported. Download only videos you have permission to save. If a site changes and extraction fails, update the package with `python -m pip install -U "yt-dlp[default]"` in the activated environment.
