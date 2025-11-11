import streamlit as st
import pandas as pd
import json
import os

# Folder where scraped data is saved
SCRAPED_DIR = "Scraped_Data"

# Streamlit page setup
st.set_page_config(
    page_title="📊 Firecrawl Data Analysis",
    page_icon="https://img.icons8.com/?size=100&id=13447&format=png&color=000000",
    layout="wide"
)

st.title("📊 Firecrawl Scraped Data Analysis")
st.write("Explore and analyze your scraped data using **Pandas** — directly from saved JSON files.")

# Step 1: List available JSON files
if not os.path.exists(SCRAPED_DIR):
    st.warning("⚠️ No 'Scraped_Data' folder found. Please scrape a website first.")
else:
    json_files = [f for f in os.listdir(SCRAPED_DIR) if f.endswith(".json")]

    if not json_files:
        st.warning("⚠️ No scraped JSON files found. Please scrape data first.")
    else:
        selected_file = st.selectbox("📂 Select a scraped data file", json_files)
        file_path = os.path.join(SCRAPED_DIR, selected_file)

        # Step 2: Load JSON data
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        st.success(f"✅ Loaded `{selected_file}` successfully!")
        st.subheader("📦 Raw Extracted JSON Data")
        st.json(data)

        # Step 3: Convert JSON to DataFrames
        st.subheader("📊 Structured Data Table")
        try:
            df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in data.items()]))
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Error converting JSON to DataFrame: {e}")

        # Step 4: Data Summary
        st.subheader("📈 Data Summary")
        counts = {k: len(v) if isinstance(v, list) else 1 for k, v in data.items()}
        summary_df = pd.DataFrame(list(counts.items()), columns=["Category", "Count"])
        st.table(summary_df)

        # Step 5: Detailed Sections
        st.divider()
        st.markdown("### 🔍 Detailed Data Views")

        col1, col2 = st.columns(2)

        with col1:
            if "headings" in data and data["headings"]:
                st.markdown("#### 🏷️ Headings")
                st.table(pd.DataFrame(data["headings"], columns=["Headings"]))
            else:
                st.info("No headings found in this dataset.")

            if "paragraphs" in data and data["paragraphs"]:
                st.markdown("#### 📄 Paragraphs")
                st.dataframe(pd.DataFrame(data["paragraphs"], columns=["Paragraphs"]))
            else:
                st.info("No paragraphs found in this dataset.")

            if "bullets" in data and data["bullets"]:
                st.markdown("#### • Bullet Points")
                st.table(pd.DataFrame(data["bullets"], columns=["Bullets"]))
            else:
                st.info("No bullet points found.")


        with col2:
            if "numbered" in data and data["numbered"]:
                st.markdown("#### 🔢 Numbered Lists")
                st.table(pd.DataFrame(data["numbered"], columns=["Numbered"]))
            else:
                st.info("No numbered lists found.")

            if "tables" in data and data["tables"]:
                st.markdown("#### 📋 Tables")
                st.dataframe(pd.DataFrame(data["tables"], columns=["Tables"]))
            else:
                st.info("No tables found.")

            if "code_blocks" in data and data["code_blocks"]:
                st.markdown("#### 💻 Code Blocks")
                for code in data["code_blocks"]:
                    st.code(code, language="python")
            else:
                st.info("No code blocks found.")

        # Step 6: Image Section
        st.divider()
        st.markdown("### 🖼️ Images")
        if "images" in data and data["images"]:
            for img in data["images"]:
                st.image(img, use_container_width=True)
        else:
            st.info("No images found in this dataset.")

        # Step 7: Download CSV
        st.divider()
        st.download_button(
            label="⬇️ Download Data as CSV",
            data=df.to_csv(index=False),
            file_name=f"{selected_file.replace('.json', '.csv')}",
            mime="text/csv"
        )