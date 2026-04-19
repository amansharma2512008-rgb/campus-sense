import streamlit as st
import pandas as pd
import requests
import streamlit.components.v1 as components

# --- YOUR LIVE RENDER LINK ---
API_URL = "https://smart-campus-api-kt8s.onrender.com/api/data"

# 1. PAGE CONFIGURATION (Force wide layout, collapse sidebar)
st.set_page_config(page_title="Custom Interface", layout="wide", initial_sidebar_state="collapsed")

# ==========================================
# 🛑 HIDE STREAMLIT'S DEFAULT UI
# ==========================================
hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;} /* Hides the top-right menu */
    header {visibility: hidden;} /* Hides the top header bar */
    footer {visibility: hidden;} /* Hides the bottom footer */
    .block-container {
        padding: 0rem !important; /* Removes all the white padding around the edges */
        max-width: 100% !important; 
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# ==========================================

# 2. FETCH THE DATA
def fetch_data():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception:
        return []

data = fetch_data()

# 3. GET THE LATEST NUMBERS (Or use defaults if no data)
if data:
    latest_temp = str(round(data[0]['temp'], 1))
    latest_hum = str(round(data[0]['hum'], 1))
    latest_time = pd.to_datetime(data[0]['timestamp']).strftime("%I:%M:%S %p")
else:
    latest_temp = "--"
    latest_hum = "--"
    latest_time = "Waiting for data..."

# 4. READ THE HTML FILE & INJECT THE DATA
try:
    with open("index.html", "r", encoding="utf-8") as file:
        raw_html = file.read()
        
        # Python replaces your {PLACEHOLDERS} with the live data!
        custom_html = raw_html.replace("{TEMP}", latest_temp)
        custom_html = custom_html.replace("{HUM}", latest_hum)
        custom_html = custom_html.replace("{TIME}", latest_time)
        
        # 5. DISPLAY THE HTML FULL SCREEN
        # We set height to 1000 pixels so it takes up the whole monitor
        components.html(custom_html, height=1000, scrolling=True)

except FileNotFoundError:
    st.error("Could not find 'index.html'. Please make sure it is in the same folder!")

