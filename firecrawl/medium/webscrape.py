import os 
import json
from dotenv import load_dotenv
from firecrawl import Firecrawl
from datetime import datetime

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

#saving scraped data
def save_data(doc: dict,base_file:str='scape_data'):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    md_path = os.path.join(Scrape_Dir,f"{base_file}_{timestamp}.md")
    json_path = os.path.join(Scrape_Dir,f"{base_file}_{timestamp}.json")

    with open(md_path,"w",encoding='utf-8') as f:
        f.write(doc.get("markdown", ""))

    with open(json_path,"w",encoding='utf-8')as f:
        json.dump(doc,f,ensure_ascii=False,indent=4)

    print(f'file saved: {md_path}')
    print(f'file saved: {json_path}')

    return json_path ,md_path