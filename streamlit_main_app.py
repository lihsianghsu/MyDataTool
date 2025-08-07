# main_app.py
import streamlit as st
import pandas as pd
from datatools.utils import log_code, reset_session, download_code_button
import importlib.util

# Initialize session state using utilities
if 'df' not in st.session_state:
    st.session_state['df'] = None
if 'df_raw' not in st.session_state:
    st.session_state['df_raw'] = None
if 'code_log' not in st.session_state:
    st.session_state['code_log'] = ["# Data processing log\n"]

# Page config
st.set_page_config(page_title="My Data Tool", layout="wide")

# Title
st.title("📊 My Data Tool")
st.markdown("A modular, interactive data preprocessing and analysis tool.")

# Progress Indicator
st.sidebar.header("Progress")
if 'df_raw' not in st.session_state or st.session_state['df_raw'] is None:
    progress = 0
    status = "📁 Load Data"
elif 'df' in st.session_state and st.session_state['df'] is not None:
    progress = 50
    status = "🧹 Data Loaded & Cleaned"
else:
    progress = 100
    status = "✅ Ready for Analysis"

st.sidebar.progress(progress)

# Navigation
st.sidebar.header("Navigation")

# Define custom pages and labels
pages = {
    "🏠 Overview": "pages/0_Overview.py",
    "1. 📁 Load Data": "pages/1_Load_Data.py",
    "2. 🔍 Explore Data": "pages/2_Explore_Data.py",
    "3. 🧹 Clean Data": "pages/3_Clean_Data.py",
    "4. 📊 Analyze Distributions": "pages/4_Analyze_Distributions.py",
    "5. 🎯 Feature vs Target": "pages/5_Feature_vs_Target.py",
    "6. 📈 Check Linearity": "pages/6_Check_Linearity.py"
}

# Default selection (first key)
default_page = list(pages.keys())[0]

# Sidebar radio with default

selection = st.sidebar.radio(
    "", 
    list(pages.keys()), 
    index=0,  # Starts with first item selected
    key="nav_radio"
)

# Reset button
st.sidebar.divider()
if st.sidebar.button("🔁 Reset Session"):
    reset_session()  # This will clear session and re-init code_log
    st.rerun()  # Use st.rerun() instead of deprecated st.experimental_rerun()

# Code Export Panel
with st.sidebar.expander("📄 View & Export Code", expanded=True):
    st.code(st.session_state.get('code_log', ['# No code']), language="python")
    download_code_button("my_data_processing.py")

# Load the selected page
try:
    with open(pages[selection], encoding="utf-8") as f:
        code = compile(f.read(), pages[selection], 'exec')
        exec(code)
except FileNotFoundError:
    st.error(f"Page not found: {pages[selection]}")
    st.markdown("Make sure the file exists in the `pages/` folder.")
except Exception as e:
    st.error(f"Error loading page: {str(e)}")