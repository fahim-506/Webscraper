import streamlit as st
import os

# Set Streamlit page config
st.set_page_config(
    page_title="Firecrawl App",
    page_icon="🔥",
    layout="wide"
)

st.title("🔥 Firecrawl Web App")
st.write("Navigate between **Web Scraper** and **Data Analysis** pages:")

# Sidebar menu
menu = ["Home", "Scraper", "Data Analysis"]
choice = st.sidebar.selectbox("📌 Menu", menu)

# Dynamic page loading
if choice == "Home":
    st.subheader("Welcome to Firecrawl!")
    st.write(
        """
        This app allows you to scrape websites for structured data and analyze the results.
        Use the menu on the left to navigate:
        - **Scraper**: Scrape websites and save structured JSON
        - **Data Analysis**: Explore and visualize your scraped data
        """
    )

elif choice == "Scraper":
    # Import scraper page
    import app
    app  # triggers Streamlit to display `app.py` content

elif choice == "Data Analysis":
    # Import data analysis page
    import data_manipulation
    data_manipulation  # triggers Streamlit to display `data_manipulation.py` contents