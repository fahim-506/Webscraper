import os
import json
from firecrawl import Firecrawl
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('FIRECRAWL_API_KEY')

Firecrawl = Firecrawl(api_key=API_KEY)
SCRAPED_DIR = "Scraped_Data"
# scraping data
def scrape_website(url: str):
    try:
        result = Firecrawl.scrape(url, formats=['markdown','html'])
        
        if hasattr(result, 'markdown') and hasattr(result, 'html'):
            return {
                'markdown':result.markdown,
                'html':result.html
            }
        else:
            return result
    except:
        print(f'Failed to scrape url {url}')
# saving scraped data
def save_scraped_data(doc: dict,base_filename: str = 'scraped_data'):
    
    md_path =os.path.join(SCRAPED_DIR, f'{base_filename}.md')
    json_path =os.path.join(SCRAPED_DIR,f'{base_filename}.json')

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(doc.get('markdown', ""))

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(doc, f,ensure_ascii=False, indent=4)


    print(f'file saved: {md_path}')
    print(f'file saved: {json_path}')


    return md_path, json_path