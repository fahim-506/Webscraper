import streamlit as st
import os
import json
import pandas as pd

st.set_page_config(layout="wide")

SCRAPED_DIR = "Scraped_Data"

st.title("📊 Scraped Data Viewer")

# -----------------------------
# ✅ Utility: Normalize data
# -----------------------------
def normalize_value(value):
    """Flatten Firecrawl structured objects into readable strings."""

    if isinstance(value, dict):
        # If object has "text"
        if "text" in value:
            return value["text"]

        # If object has "code"
        if "code" in value:
            return value["code"]

        # Other dict → convert to string
        return json.dumps(value)

    elif isinstance(value, list):
        # Normalize each element inside lists
        return [normalize_value(v) for v in value]

    return value


if not os.path.exists(SCRAPED_DIR):
    st.warning("No scraped data found. Run scraper first.")
else:
    files = [f for f in os.listdir(SCRAPED_DIR) if f.endswith(".json")]

    if not files:
        st.warning("No JSON files found.")
    else:
        selected = st.selectbox("Select a JSON file", files)
        filepath = os.path.join(SCRAPED_DIR, selected)

        with open(filepath, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        st.success(f"Loaded `{selected}`")

        # -----------------------------
        # ✅ Normalize the entire JSON
        # -----------------------------
        data = {k: normalize_value(v) for k, v in raw_data.items()}

        st.subheader("📦 Cleaned JSON Data")
        st.json(data)

        # -----------------------------
        # ✅ Convert to table safely
        # -----------------------------
        try:
            df = pd.DataFrame({
                k: pd.Series(v) if isinstance(v, list) else pd.Series([v])
                for k, v in data.items()
            })
            st.subheader("📊 Structured Tables")
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Error generating table: {e}")

        st.subheader("🔍 Individual Sections")

        # -----------------------------
        # ✅ Headings Table
        # -----------------------------
        if "headings" in data and data["headings"]:
            st.markdown("### 🏷 Headings")
            headings_df = pd.DataFrame(data["headings"], columns=["Heading"])
            st.table(headings_df)
        else:
            st.info("No headings found.")

        # -----------------------------
        # ✅ Paragraphs Table
        # -----------------------------
        if "paragraphs" in data and data["paragraphs"]:
            st.markdown("### 📄 Paragraphs")
            paragraphs_df = pd.DataFrame(data["paragraphs"], columns=["Paragraph"])
            st.dataframe(paragraphs_df, use_container_width=True)
        else:
            st.info("No paragraphs found.")

        # -----------------------------
        # ✅ Code Blocks Table
        # -----------------------------
        if "code_blocks" in data and data["code_blocks"]:
            st.markdown("### 💻 Code Blocks")
            for block in data["code_blocks"]:
                st.code(block, language="python")
        else:
            st.info("No code blocks found.")

        # -----------------------------
        # ✅ CSV Download
        # -----------------------------
        if 'df' in locals():
            st.download_button(
                "Download CSV",
                data=df.to_csv(index=False),
                file_name=selected.replace(".json", ".csv"),
                mime="text/csv",
            )
