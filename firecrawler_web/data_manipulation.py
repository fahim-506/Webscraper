import streamlit as st
import pandas as pd
import json
import os

SCRAPED_DIR = "Scraped_Data"

def run_data_analysis_page():
    st.title("📊 Firecrawl Scraped Data Analysis")
    st.write("Explore and analyze your scraped data using **Pandas** — directly from saved JSON files.")

    if not os.path.exists(SCRAPED_DIR):
        st.warning("⚠️ No 'Scraped_Data' folder found. Please scrape a website first.")
        return

    json_files = [f for f in os.listdir(SCRAPED_DIR) if f.endswith(".json")]

    if not json_files:
        st.warning("⚠️ No scraped JSON files found. Please scrape data first.")
        return

    selected_file = st.selectbox("📂 Select a scraped data file", json_files)
    file_path = os.path.join(SCRAPED_DIR, selected_file)

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    st.success(f"✅ Loaded `{selected_file}` successfully!")
    st.subheader("📦 Raw Extracted JSON Data")
    st.json(data)

    # Convert JSON → DataFrame
    st.subheader("📊 Structured Data Table")
    try:
        df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in data.items()]))
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Error converting JSON to DataFrame: {e}")

    # Summary
    st.subheader("📈 Data Summary")
    counts = {k: len(v) if isinstance(v, list) else 1 for k, v in data.items()}
    summary_df = pd.DataFrame(list(counts.items()), columns=["Category", "Count"])
    st.table(summary_df)

    # Detailed Views
    st.divider()
    st.markdown("### 🔍 Detailed Data Views")

    col1, col2 = st.columns(2)
    with col1:
        if "headings" in data and data["headings"]:
            st.markdown("#### 🏷️ Headings")
            st.table(pd.DataFrame(data["headings"], columns=["Headings"]))
        if "paragraphs" in data and data["paragraphs"]:
            st.markdown("#### 📄 Paragraphs")
            st.dataframe(pd.DataFrame(data["paragraphs"], columns=["Paragraphs"]))
        if "bullets" in data and data["bullets"]:
            st.markdown("#### • Bullet Points")
            st.table(pd.DataFrame(data["bullets"], columns=["Bullets"]))

    with col2:
        if "numbered" in data and data["numbered"]:
            st.markdown("#### 🔢 Numbered Lists")
            st.table(pd.DataFrame(data["numbered"], columns=["Numbered"]))
        if "tables" in data and data["tables"]:
            st.markdown("#### 📋 Tables")
            st.dataframe(pd.DataFrame(data["tables"], columns=["Tables"]))
        if "code_blocks" in data and data["code_blocks"]:
            st.markdown("#### 💻 Code Blocks")
            for code in data["code_blocks"]:
                st.code(code, language="python")

    # Images
    st.divider()
    st.markdown("### 🖼️ Images")
    if "images" in data and data["images"]:
        for img in data["images"]:
            st.image(img, use_container_width=True)
    else:
        st.info("No images found.")

    # CSV Download
    st.divider()
    st.download_button(
        label="⬇️ Download Data as CSV",
        data=df.to_csv(index=False),
        file_name=f"{selected_file.replace('.json', '.csv')}",
        mime="text/csv"
    )
