import streamlit as st
from web_scraping import scrape_website, save_scraped_data
import json

st.title("🕸️ Firecrawl Scraper")

url = st.text_input("Enter URL", placeholder="https://example.com")

if st.button("Scrape Now"):
    if not url:
        st.warning("Please enter a valid URL")
    else:
        with st.spinner("Scraping website..."):
            data = scrape_website(url)

        if not data:
            st.error("Scrape failed.")
        else:
            st.success("✅ Scrape Successful!")

            save_path = save_scraped_data(data)
            st.info(f"Saved to: `{save_path}`")

            st.subheader("📦 Extracted JSON")
            st.json(data)

            # Human-Readable formatted text
            st.subheader("🧾 Readable Extracted Content")

            readable = ""

            if data.get("headings"):
                readable += "### Headings\n" + "\n".join(f"- {h}" for h in data["headings"]) + "\n\n"

            if data.get("paragraphs"):
                readable += "### Paragraphs\n" + "\n".join(f"- {p}" for p in data["paragraphs"]) + "\n\n"

            if data.get("code_blocks"):
                readable += "### Code Blocks\n"
                for block in data["code_blocks"]:
                    readable += f"```python\n{block}\n```\n\n"

            st.markdown(readable)
