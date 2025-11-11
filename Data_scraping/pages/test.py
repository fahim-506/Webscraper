import streamlit as st
import os
import json
import pandas as pd

st.set_page_config(layout="wide")

SCRAPED_DIR = "Scraped_Data"
combined_data = {
     "title" : [],
     "headings" : []
}
st.title("📊 Scraped Data Viewer")

if not os.path.exists(SCRAPED_DIR):
    st.warning("No scraped data found. Run scraper first.")
else:
        for filename in os.listdir(SCRAPED_DIR):
            if filename.endswith(".json"):
                file_path = os.path.join(SCRAPED_DIR, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    dicti = json.load(f)
                    combined_data['title'] = [item['text'] for item in dicti['headings']]
                    print(f"output: {combined_data}")


        print(combined_data)
        st.write(combined_data)



