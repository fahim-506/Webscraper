import streamlit as st
import json
import pandas as pd
import re
from web_scraping import scrape_website, save_scraped_data

# Streamlit setup
st.set_page_config(page_title='Firecrawl scraper', page_icon='https://img.icons8.com/?size=100&id=13447&format=png&color=000000', layout='wide')
st.title('Firecrawl Web Scraper')
st.write('Paste website link below to scrape structured data')

url = st.text_input('Enter a website URL', placeholder="https://example.com")
# Utility: Extract structured content (headings, lists, tables, code)
def extract_structured_content(markdown_text: str):
    lines = markdown_text.split("\n")
    structured = []
    inside_code = False

    for line in lines:
        # detect code blocks
        if line.strip().startswith("```"):
            inside_code = not inside_code
            structured.append(line)
            continue

        if inside_code or re.match(r"^#{1,6}\s", line) or re.match(r"^\s*[-*•]\s", line) or re.match(r"^\s*\d+\.\s", line) or re.match(r"^\s*\|.*\|", line):
            structured.append(line)

    return "\n".join(structured).strip()


# Scrape button
if st.button('Scrape Now'):
    if not url.strip():
        st.warning('⚠️ Please enter a valid URL')
    else:
        with st.spinner('⏳ Scraping data... please wait'):
            try:
                scraped_data = scrape_website(url)
                if scraped_data:
                    st.success('✅ Scrape completed successfully!')
                    
                    # Save the scraped JSON
                    file_path = save_scraped_data(scraped_data)

                    # Extract markdown text if present
                    markdown_text = scraped_data.get('markdown', '')
                    if not markdown_text:
                        markdown_text = json.dumps(scraped_data, indent=2)  # fallback

                    # Filter structured content
                    filtered_md = extract_structured_content(markdown_text)

                    st.subheader("🧾 Extracted Structured Content")
                    st.markdown(filtered_md)

                    with st.expander("📄 View Full JSON"):
                        st.json(scraped_data)
                    
                    st.info(f"Saved to: `{file_path}`")
                else:
                    st.error("❌ No data scraped or invalid response.")
            except Exception as e:
                st.error(f'❌ Error: {e}')
