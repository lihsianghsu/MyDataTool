# pages/2_Explore_Data.py
import streamlit as st
import numpy as np
from datatools.analyzer import generate_column_info, summarize_dataset

st.header("🔍 Explore Data")
st.markdown("Automated EDA report of your dataset.")

if 'df' in st.session_state:
    df = st.session_state['df']

    st.subheader("📋First few rows:")
    st.dataframe(df.head())

    st.subheader("📊 Column Summary")
    column_info = generate_column_info(df)
    st.dataframe(column_info)

    st.subheader("🧾 Dataset Summary")
    summary = summarize_dataset(df)
    summary_clean = {k: int(v) if isinstance(v, (np.integer, np.int64, np.floating, np.float64)) else v for k, v in summary.items()}
    st.json(summary_clean)
    #st.table(summary)

else:
    st.warning("Please upload a dataset in the 'Load Data' tab first.")