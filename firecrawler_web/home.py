import streamlit as st
import home
import data_manipulation
import app


# Initialize page in session state
if "page" not in st.session_state:
    st.session_state.page = "home"

# Navigation buttons in sidebar
st.sidebar.title("Navigation")
if st.sidebar.button("🏠 Home"):
    st.session_state.page = "home"
if st.sidebar.button("ℹ️ Scrape Data"):
    st.session_state.page = "app"
if st.sidebar.button("📞 Data Manipulation"):
    st.session_state.page = "data_manipulation"

# Page routing
if st.session_state.page == "home":
    home.show()
elif st.session_state.page == "app":
    app.show()
elif st.session_state.page == "data_manipulation":
    data_manipulation.show()

