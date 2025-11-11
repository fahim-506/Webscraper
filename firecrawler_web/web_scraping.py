import os
import json
from firecrawl import Firecrawl
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

API_KEY = os.getenv('FIRECRAWL_API_KEY')
firecrawl_client = Firecrawl(api_key=API_KEY)

SCRAPED_DIR = "Scraped_Data"
os.makedirs(SCRAPED_DIR, exist_ok=True)

# Scrape website and get structured JSON
def scrape_website(url: str):
    try:
        result = firecrawl_client.scrape(url, formats=[{
            "type": "json",
            "prompt": ( 
                "Extract structured data from the webpage, including "
                "headings, paragraphs,"
                 "code blocks."         #image URLs.,   tables,  bullet points. links . numbered lists,  
                ),
            "schema": {
                "headings": {"type": "array", "items": {"type": "string"}},
                "code_blocks": {"type": "array", "items": {"type": "string"}},
                "paragraphs": {"type": "array", "items": {"type": "string"}},
                # "numbered": {"type": "array", "items": {"type": "string"}}, 
                # "links": {"type": "array", "items": {"type": "string"}},
                # "bullets": {"type": "array", "items": {"type": "string"}},
                # "tables": {"type": "array", "items": {"type": "string"}},
                # "images": {"type": "array", "items": {"type": "string"}}
            }
        }])

        # Handle both dict or object response
        if isinstance(result, dict):
            return result
        elif hasattr(result, 'json'):
            return result.json
        else:
            print("⚠️ Unexpected result format:", type(result))
            return None

    except Exception as e:
        print(f'❌ Failed to scrape url {url}: {e}')
        return None


# Optional: Save scraped data to JSON file
def save_scraped_data(doc: dict, base_filename: str = 'Data'):
    # Ensure the save directory exists
    os.makedirs(SCRAPED_DIR, exist_ok=True)

    # Count how many JSON files already exist
    existing_files = [
        f for f in os.listdir(SCRAPED_DIR)
        if f.startswith(base_filename) and f.endswith(".json")
    ]

    # Determine next index number
    next_index = len(existing_files) + 1

    # Create the new filenames
    json_path = os.path.join(SCRAPED_DIR, f"{base_filename}_{next_index}.json")

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(doc, f, ensure_ascii=False, indent=4)

    print(f'✅ File saved: {json_path}')
    return json_path
