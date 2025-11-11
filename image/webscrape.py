import re
import os
# import json
from urllib.parse import urljoin
from firecrawl import Firecrawl
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FIRECRAWL_API_KEY")
firecrawl_client = Firecrawl(api_key=API_KEY)

SCRAPED_DIR = "Scraped_Data"
os.makedirs(SCRAPED_DIR, exist_ok=True)


def get_images(url: str):
    """
    Request raw_html from Firecrawl and extract image URLs.
    Returns a list of fully-qualified image URLs.
    """
    try:
        # ask for raw_html (literal name used by Firecrawl v2)
        result = firecrawl_client.scrape(url, formats=["raw_html"])
    except Exception as exc:
        print(f"Failed to fetch raw_html: {exc}")
        return []

    # try to access raw_html from several possible shapes
    html = None
    if isinstance(result, dict):
        html = result.get(
            "raw_html") or result.get("raw") or result.get("html")
    else:
        html = getattr(result, "raw_html", None)
        if not html:
            html = getattr(result, "raw", None)
        if not html:
            html = getattr(result, "html", None)

    if not html:
        return []

    # capture src and common lazy-src attributes (data-src, data-lazy-src)
    pattern = (
        r'<img[^>]+'
        r'(?:src|data-src|data-lazy-src|data-srcset)'
        r'\s*=\s*["\']'
        r'([^"\'>]+)'
        r'["\']'
        )
    image_urls = re.findall(pattern, html, flags=re.IGNORECASE)

    final_urls = []
    for img in image_urls:
        if img.startswith("//"):
            img = "https:" + img
        elif img.startswith("/"):
            img = urljoin(url, img)
        final_urls.append(img)

    # deduplicate while preserving order
    seen = set()
    deduped = []
    for u in final_urls:
        if u not in seen:
            seen.add(u)
            deduped.append(u)

    return deduped
