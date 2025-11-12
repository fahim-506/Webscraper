import re
import os
from urllib.parse import urljoin
from firecrawl import Firecrawl
from dotenv import load_dotenv
import streamlit as st

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
            "raw_html") or result.get(
                "raw") or result.get(
                    "html")
    else:
        html = getattr(result, "raw_html", None)
        if not html:
            html = getattr(result, "raw", None)
        if not html:
            html = getattr(result, "html", None)

    if not html:
        return []

    # capture src and common lazy-src attributes
    # (data-src, data-lazy-src, data-srcset)
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


st.set_page_config(page_title="Firecrawl scraper", layout="wide")
st.title("Firecrawl Image Viewer")
st.write("Images are shown for the last URL scraped from the Scraper page.")

# Get URL from session_state or fallback to the last_scraped_url file
url = None
if "last_scraped_url" in st.session_state:
    url = st.session_state["last_scraped_url"]
else:
    last_file = os.path.join(SCRAPED_DIR, "last_scraped_url.txt")
    if os.path.exists(last_file):
        try:
            with open(last_file, "r") as f:
                url = f.read().strip()
        except Exception:
            url = None

if not url:
    st.warning(
        "No images available. Go to the Scraper page and scrape a URL first.")
else:
    with st.spinner("Finding images..."):
        images = get_images(url)

    if not images:
        st.warning(f"No images found for: {url}")
    else:
        st.success(f"Found {len(images)} images from {url}")

        # allow user to control image width
        img_width = st.slider(
            "adjust the width (pixels)",
            min_value=100, max_value=1200,
            value=400
        )

        cols = st.columns(3)
        for i, img in enumerate(images):
            with cols[i % 3]:
                st.image(img, width=img_width)
