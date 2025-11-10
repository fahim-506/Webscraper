import streamlit as st
import json
from webscrape import scrape_web,save_data
import pandas as pd

st.set_page_config(page_title='Firecrawl scraper',page_icon='⌨️',layout='wide')
st.title('Firecrawl Web Scraper')
st.write('paste website link below')

url = st.text_input('Enter a website URL',placeholder="https://example.com")

if st.button('scrape now'):
    if not url.strip():
        st.warning('Please enter valid URL')
    else:
        with st.spinner('Data is scraping...'):
            try:
                scraped_data= scrape_web(url)
                st.success("Scrape completed.")
                st.subheader('Markdown Output')
                st.markdown(scraped_data['markdown'])

                with st.expander('Show Raw HTML'):
                    st.code(scraped_data['html'],language="html")
                    md_file, json_file =save_data(scraped_data)

            except Exception as e:
                st.error(f'error: {e}')

