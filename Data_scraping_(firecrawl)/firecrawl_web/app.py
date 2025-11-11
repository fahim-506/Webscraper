import streamlit as st

st.set_page_config(page_title="🔥 Firecrawl App", layout="wide")

# -----------------------------------------------------
# 🏠 HOME PAGE (About Project)
# -----------------------------------------------------
st.title("🔥 Firecrawl Data Suite")
st.write("""
Welcome to **Firecrawl**, a streamlined platform for intelligent web data extraction and analysis.  
This tool empowers you to:
- 🕸️ **Scrape structured web content** like headings, paragraphs, and code blocks  
- 📊 **Analyze and visualize scraped data** quickly and efficiently  
- 💾 **Save results automatically** as JSON files for later exploration  
""")

st.divider()

st.markdown("### 🚀 Quick Start")
st.markdown("""
1. Go to the **Web Scraper** page (see sidebar) to extract structured data from any webpage.  
2. Visit **Data Manipulation** to explore, filter, and download scraped data.  
3. Saved files will appear automatically in your `Scraped_Data/` folder.
""")

st.info("👉 Use the sidebar on the left to navigate between tools.")

st.divider()

st.markdown("### 🧠 Features")
st.markdown("""
- **One-click scraping** powered by Firecrawl API  
- **JSON data export** for structured web content  
- **Interactive analysis dashboard** using Pandas + Streamlit  
- **Expandable architecture** — easily add new modules
""")

st.divider()
st.caption("© 2025 Firecrawl Data Suite | Built with  using Streamlit developed : Fahim , Hafiz, Thameem")

