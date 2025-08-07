# pages/1_Load_Data.py
import streamlit as st
import pandas as pd
from datatools.loader import load_dataframe
from datatools.utils import log_code, reset_session, download_code_button

st.header("📁 Load Data")
st.markdown("Upload your dataset below.")

uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "json"])

# Track code
log_code("df = pd.read_csv('data.csv')")

if uploaded_file is not None:
    file_type = uploaded_file.name.split('.')[-1]

    if file_type == 'csv':
        separator = st.text_input("Enter CSV separator (default is ',')", value=",")
        df = load_dataframe(uploaded_file, filetype='csv', sep=separator)
    else:
        df = load_dataframe(uploaded_file, filetype=file_type)

    st.success("✅ File loaded successfully!")

    st.subheader("First few rows:")
    st.dataframe(df.head())

    st.session_state['df_raw'] = df.copy()
    st.session_state['df'] = df.copy()

    st.info("You can now proceed to 'Explore Data' or 'Clean Data'.")
else:
    st.warning("No file uploaded yet.")