"""Find an HLS playlist requested by a video page in Chrome."""

from time import monotonic
from urllib.parse import urlsplit


def find_hls_url(page_url, timeout_seconds=30, headless=False):
    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError, sync_playwright

    found = []

    def on_response(response):
        content_type = response.headers.get("content-type", "").lower()
        if response.status < 400 and (
            ".m3u8" in urlsplit(response.url).path.lower() or "mpegurl" in content_type
        ):
            found.append(response.url)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless) # channel="chrome", remove this if using WSL

        try:
            context = browser.new_context()
            context.on("response", on_response)
            page = context.new_page()
            try:
                page.goto(page_url, wait_until="domcontentloaded", timeout=timeout_seconds * 1000)
            except PlaywrightTimeoutError:
                pass
            deadline = monotonic() + timeout_seconds
            while not found and monotonic() < deadline and not page.is_closed():
                page.wait_for_timeout(250)
            return found[0] if found else None
        finally:
            browser.close()
