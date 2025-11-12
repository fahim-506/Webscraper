import os
import json
from firecrawl import Firecrawl
from dotenv import load_dotenv 

load_dotenv()

API_KEY = os.getenv("FIRECRAWL_API_KEY")
firecrawl_client = Firecrawl(api_key=API_KEY)

SCRAPED_DIR = "Scraped_Data"
os.makedirs(SCRAPED_DIR, exist_ok=True)


def scrape_website(url: str):
    """Scrapes website and returns structured JSON."""
    try:
        result = firecrawl_client.scrape(
            url,
            formats=[{
                "type": "json",
                "prompt": (
                    "Extract structured data: headings, paragraphs, code blocks."
                ),
                "schema": {
                    "headings": {"type": "array", "items": {"type": "string"}},
                    "paragraphs": {"type": "array", "items": {"type": "string"}},
                    "code_blocks": {"type": "array", "items": {"type": "string"}},
                }
            }]
        )

        if isinstance(result, dict):
            return result
        elif hasattr(result, "json"):
            return result.json
        else:
            return None

    except Exception as e:
        print("Scrape failed:", e)
        return None


def save_scraped_data(data: dict, base: str = "Scrape"):
    """Saves JSON with incremental numbering."""
    files = [f for f in os.listdir(SCRAPED_DIR) if f.startswith(base)]
    new_index = len(files) + 1

    filepath = os.path.join(SCRAPED_DIR, f"{base}_{new_index}.json")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return filepath
