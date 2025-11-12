import streamlit as st
import os
import json
import pandas as pd

st.set_page_config(layout="wide")

SCRAPED_DIR = "Scraped_Data"
combined_data = {
    "headings": [],
    "paragraphs": [],
}

st.title("📊 Scraped Data Viewer")

if not os.path.exists(SCRAPED_DIR):
    st.warning("No scraped data found. Run scraper first.")
else:
    for filename in os.listdir(SCRAPED_DIR):
        if filename.endswith(".json"):
            file_path = os.path.join(SCRAPED_DIR, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                dicti = json.load(f)

                # Safely extract lists
                headings = [item.get("text", "") for item in dicti.get("headings", [])]
                paragraphs = [item.get("text", "") for item in dicti.get("paragraphs", [])]

                # Append (not overwrite)
                combined_data["headings"].extend(headings)
                combined_data["paragraphs"].extend(paragraphs)

    # Show in Streamlit
    max_len = max(len(combined_data["headings"]), len(combined_data["paragraphs"]))

        # Pad shorter list with empty strings
    for key in combined_data:
            while len(combined_data[key]) < max_len:
                combined_data[key].append("")

    df = pd.DataFrame(combined_data)

    st.subheader(" 🎉 Finally I Got It!")

    df = pd.DataFrame(combined_data)
    st.dataframe(df, use_container_width=True)