from webscrape import get_images, scrape_website, save_scraped_data
import streamlit as st
import json
import re

st.set_page_config(page_title="Firecrawl scraper", layout="wide")
st.title("Firecrawl Web Scraper")
st.write("Paste website link below to scrape structured data")

url = st.text_input("Enter a website URL", placeholder="https://example.com")


def extract_structured_content(markdown_text: str):
    """
    Return only headings, list items, numbered lines, tables, and code
    blocks from a block of markdown/text.
    """
    lines = markdown_text.split("\n")
    structured = []
    inside_code = False

    for line in lines:
        if line.strip().startswith("```"):
            inside_code = not inside_code
            structured.append(line)
            continue

        if (
            inside_code
            or re.match(r"^#{1,6}\s", line)
            or re.match(r"^\s*[-*•]\s", line)
            or re.match(r"^\s*\d+\.\s", line)
            or re.match(r"^\s*\|.*\|", line)
        ):
            structured.append(line)

    return "\n".join(structured).strip()


if st.button("Scrape Now"):
    if not url.strip():
        st.warning("Please enter a valid URL")
    else:
        with st.spinner("Scraping data..."):
            scraped_data = scrape_website(url)

        if scraped_data:
            st.success("Scrape completed successfully")
            file_path = save_scraped_data(scraped_data)

            # If 'markdown' key exists, use it; otherwise pretty JSON
            markdown_text = scraped_data.get("markdown", "")
            if not markdown_text:
                markdown_text = json.dumps(scraped_data, indent=2)

            filtered_md = extract_structured_content(markdown_text)

            st.subheader("Extracted Structured Content")
            st.markdown(filtered_md)

            with st.expander("View Full JSON"):
                st.json(scraped_data)

            st.info(f"Saved to: `{file_path}`")
        else:
            st.error("Scrape failed.")


st.title("Firecrawl Image Viewer")

if url:
    with st.spinner("Finding images..."):
        images = get_images(url)

    if not images:
        st.warning("No images found.")
    else:
        st.success(f"Found {len(images)} images")

        # allow user to control image width
        img_width = st.slider(
            "Image display width (pixels)",
            min_value=100, max_value=1200,
            value=400
        )

        cols = st.columns(3)
        for i, img in enumerate(images):
            with cols[i % 3]:
                st.image(img, width=img_width)
