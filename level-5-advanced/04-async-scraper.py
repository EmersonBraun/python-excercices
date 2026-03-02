"""
Level 5 - Exercise 04: Async Web Scraper (Simulated)
=====================================================

Difficulty: 4/5 stars
Estimated time: 25 minutes

Learn asyncio fundamentals by building a simulated async web scraper.
No real HTTP calls are made -- we use asyncio.sleep to mimic network
latency and return mock HTML/data.

Exercises
---------
1. Mock HTTP client   - async function that simulates fetching a URL.
2. parse_page         - Extracts "links" and "title" from mock HTML.
3. async_scraper      - Orchestrates concurrent fetching of multiple pages.
4. rate_limited_fetch - Fetches with a semaphore to limit concurrency.

Expected output (approximate):
------------------------------
# Fetching 5 pages concurrently...
# [0.51s] Fetched https://example.com/page/1  (title: Page 1)
# [0.32s] Fetched https://example.com/page/2  (title: Page 2)
# ...
# All 5 pages fetched in 0.53s  (parallel is faster than serial!)

# Rate-limited (max 2 concurrent):
# Fetched batch of 5 pages in ~1.2s
"""

import asyncio
import random
import time


# ---------------------------------------------------------------------------
# Mock data -- simulates what a real HTTP response might look like
# ---------------------------------------------------------------------------
MOCK_PAGES = {
    "https://example.com/page/1": {
        "status": 200,
        "html": "<html><title>Page 1</title><body>"
                '<a href="/page/2">Next</a>'
                '<a href="/about">About</a>'
                "</body></html>",
        "latency": 0.3,
    },
    "https://example.com/page/2": {
        "status": 200,
        "html": "<html><title>Page 2</title><body>"
                '<a href="/page/3">Next</a>'
                "</body></html>",
        "latency": 0.5,
    },
    "https://example.com/page/3": {
        "status": 200,
        "html": "<html><title>Page 3</title><body>"
                '<a href="/page/1">Home</a>'
                '<a href="/contact">Contact</a>'
                "</body></html>",
        "latency": 0.2,
    },
    "https://example.com/about": {
        "status": 200,
        "html": "<html><title>About Us</title><body>"
                "<p>We are example.com</p>"
                "</body></html>",
        "latency": 0.15,
    },
    "https://example.com/contact": {
        "status": 200,
        "html": "<html><title>Contact</title><body>"
                "<p>Email: info@example.com</p>"
                "</body></html>",
        "latency": 0.25,
    },
}


# ---------------------------------------------------------------------------
# 1. Mock HTTP Client
# ---------------------------------------------------------------------------
async def mock_fetch(url: str) -> dict:
    """Simulate an async HTTP GET request.

    Returns a dict with 'status', 'html', and 'url' keys.
    Raises RuntimeError for unknown URLs (simulates 404).
    """
    page = MOCK_PAGES.get(url)
    if page is None:
        await asyncio.sleep(0.1)
        raise RuntimeError(f"404 Not Found: {url}")

    # Simulate network latency with some jitter
    latency = page["latency"] + random.uniform(-0.05, 0.05)
    await asyncio.sleep(max(0.05, latency))
    return {"status": page["status"], "html": page["html"], "url": url}


# ---------------------------------------------------------------------------
# 2. Parse Page (extract title and links from mock HTML)
# ---------------------------------------------------------------------------
def parse_page(html: str) -> dict:
    """Extract a title and links from a simple HTML string.

    Uses basic string operations (no external HTML parser needed
    for this mock data).

    >>> parse_page('<html><title>Hello</title><a href="/x">X</a></html>')
    {'title': 'Hello', 'links': ['/x']}
    """
    # Extract title
    title = ""
    start = html.find("<title>")
    end = html.find("</title>")
    if start != -1 and end != -1:
        title = html[start + 7:end]

    # Extract href values
    links = []
    search_from = 0
    while True:
        idx = html.find('href="', search_from)
        if idx == -1:
            break
        idx += 6
        end_idx = html.find('"', idx)
        if end_idx == -1:
            break
        links.append(html[idx:end_idx])
        search_from = end_idx + 1

    return {"title": title, "links": links}


# ---------------------------------------------------------------------------
# 3. Async Scraper  (concurrent fetch of multiple URLs)
# ---------------------------------------------------------------------------
async def async_scraper(urls: list[str]) -> list[dict]:
    """Fetch and parse multiple URLs concurrently.

    Returns a list of dicts: {'url', 'title', 'links', 'elapsed'}.
    """
    async def fetch_and_parse(url):
        start = time.perf_counter()
        try:
            response = await mock_fetch(url)
            parsed = parse_page(response["html"])
            elapsed = time.perf_counter() - start
            return {
                "url": url,
                "title": parsed["title"],
                "links": parsed["links"],
                "elapsed": elapsed,
                "error": None,
            }
        except Exception as exc:
            elapsed = time.perf_counter() - start
            return {
                "url": url,
                "title": None,
                "links": [],
                "elapsed": elapsed,
                "error": str(exc),
            }

    tasks = [fetch_and_parse(url) for url in urls]
    return await asyncio.gather(*tasks)


# ---------------------------------------------------------------------------
# 4. Rate-Limited Fetch (semaphore)
# ---------------------------------------------------------------------------
async def rate_limited_scraper(urls: list[str], max_concurrent: int = 2) -> list[dict]:
    """Like async_scraper but limits concurrency with a semaphore.

    At most *max_concurrent* requests are in flight at the same time.
    """
    semaphore = asyncio.Semaphore(max_concurrent)

    async def limited_fetch(url):
        async with semaphore:
            start = time.perf_counter()
            try:
                response = await mock_fetch(url)
                parsed = parse_page(response["html"])
                elapsed = time.perf_counter() - start
                return {
                    "url": url,
                    "title": parsed["title"],
                    "links": parsed["links"],
                    "elapsed": elapsed,
                    "error": None,
                }
            except Exception as exc:
                elapsed = time.perf_counter() - start
                return {
                    "url": url,
                    "title": None,
                    "links": [],
                    "elapsed": elapsed,
                    "error": str(exc),
                }

    tasks = [limited_fetch(url) for url in urls]
    return await asyncio.gather(*tasks)


# ===================================================================
# Demo / self-test
# ===================================================================
async def main():
    urls = list(MOCK_PAGES.keys())

    # --- Unrestricted concurrent fetch ---
    print("=" * 60)
    print("Async Scraper  (all concurrent)")
    print("=" * 60)
    overall_start = time.perf_counter()
    results = await async_scraper(urls)
    overall_elapsed = time.perf_counter() - overall_start

    for r in results:
        if r["error"]:
            print(f"  [{r['elapsed']:.2f}s] ERROR {r['url']}: {r['error']}")
        else:
            print(f"  [{r['elapsed']:.2f}s] {r['url']}  ->  title='{r['title']}', "
                  f"links={r['links']}")
    print(f"\nAll {len(urls)} pages fetched in {overall_elapsed:.2f}s\n")

    # --- Rate-limited fetch ---
    print("=" * 60)
    print("Rate-Limited Scraper  (max 2 concurrent)")
    print("=" * 60)
    overall_start = time.perf_counter()
    results = await rate_limited_scraper(urls, max_concurrent=2)
    overall_elapsed = time.perf_counter() - overall_start

    for r in results:
        if r["error"]:
            print(f"  [{r['elapsed']:.2f}s] ERROR {r['url']}: {r['error']}")
        else:
            print(f"  [{r['elapsed']:.2f}s] {r['url']}  ->  title='{r['title']}'")
    print(f"\nAll {len(urls)} pages fetched in {overall_elapsed:.2f}s (rate-limited)\n")

    # --- Handling errors ---
    print("=" * 60)
    print("Error Handling  (includes a bad URL)")
    print("=" * 60)
    bad_urls = ["https://example.com/page/1", "https://example.com/nonexistent"]
    results = await async_scraper(bad_urls)
    for r in results:
        if r["error"]:
            print(f"  FAIL: {r['url']} -> {r['error']}")
        else:
            print(f"  OK:   {r['url']} -> {r['title']}")


if __name__ == "__main__":
    asyncio.run(main())
