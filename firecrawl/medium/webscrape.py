import os 
import json
from dotenv import load_dotenv
from firecrawl import Firecrawl

load_dotenv()

app = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))

Scrape_Dir = "Scraped_Data"
#scraping data
def scrape_web(url: str):
    try:
        result = app.scrape(url ,formats=["markdown","html"])
        if hasattr(result,"markdown")and hasattr(result,"html"):
            return {
                'markdown':result.markdown,
                'html':result.html
            }
        else:
            return result

    except:
        print(f"Failed to scrape url{url}")

