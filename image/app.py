from webscrape import get_images
import streamlit as st
# import json
# import re

st.set_page_config(page_title="Firecrawl scraper", layout="wide")
st.title("Firecrawl Image Viewer")
st.write("Paste website link below to scrape image")

url = st.text_input("Enter a website URL", placeholder="https://example.com")


if url:
    with st.spinner("Finding images..."):
        images = get_images(url)

    if not images:
        st.warning("No images found.")
    else:
        st.success(f"Found {len(images)} images")

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
