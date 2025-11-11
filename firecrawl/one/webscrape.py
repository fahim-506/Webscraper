import re
import os
import json
from urllib.parse import urljoin
from firecrawl import Firecrawl
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FIRECRAWL_API_KEY")
firecrawl_client = Firecrawl(api_key=API_KEY)

SCRAPED_DIR = "Scraped_Data"
os.makedirs(SCRAPED_DIR, exist_ok=True)


def _normalize_result(obj):
    """
    Convert Firecrawl return objects (pydantic Document or similar)
    into a standard Python dict/list/str so it can be JSON serialized.
    """
    if obj is None:
        return None

    # If it's already a plain dict/list/str/number, return as is
    if isinstance(obj, (dict, list, str, int, float, bool)):
        return obj

    # pydantic v2 uses model_dump()
    if hasattr(obj, "model_dump"):
        try:
            return obj.model_dump()
        except Exception:
            pass

    # Fallback to dict() if available
    if hasattr(obj, "dict"):
        try:
            return obj.dict()
        except Exception:
            pass

    # Fallback to json() then load
    if hasattr(obj, "json"):
        try:
            return json.loads(obj.json())
        except Exception:
            pass

    # Last resort: string representation
    return {"value": str(obj)}


def scrape_website(url: str):
    """
    Scrape a page and return a normalized Python dict (structured json).
    Uses the JSON format with a simple schema prompt.
    """
    try:
        result = firecrawl_client.scrape(
            url,
            formats=[
                {
                    "type": "json",
                    "prompt": (
                        "Extract structured data from the webpage. Include headings, "
                        "paragraphs and code blocks where present."
                    ),
                    "schema": {
                        "headings": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "code_blocks": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "paragraphs": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                    },
                }
            ],
        )
        return _normalize_result(result)

    except Exception as exc:
        print(f"Failed to scrape url {url}: {exc}")
        return None


def save_scraped_data(doc, base_filename: str = "Data"):
    """
    Save normalized scraped data to a JSON file.
    """
    normalized = _normalize_result(doc)

    os.makedirs(SCRAPED_DIR, exist_ok=True)

    existing_files = [
        f for f in os.listdir(SCRAPED_DIR)
        if f.startswith(base_filename) and f.endswith(".json")
    ]

    next_index = len(existing_files) + 1
    json_path = os.path.join(SCRAPED_DIR, f"{base_filename}_{next_index}.json")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(normalized, f, ensure_ascii=False, indent=4)

    print(f"File saved: {json_path}")
    return json_path


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
    pattern = r'<img[^>]+(?:src|data-src|data-lazy-src|data-srcset)\s*=\s*["\']([^"\'>]+)["\']'
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
