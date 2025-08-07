# pages/0_Overview.py
import streamlit as st
import pandas as pd

st.header("🏠 Welcome to My Data Tool")
st.markdown("""
This interactive tool helps you:
- Load, explore, and clean datasets
- Visualize distributions and correlations
- Perform statistical tests (ANOVA, normality, linearity, feature vs target)
- Export your workflow as Python code

Navigate using the sidebar to begin.
""")

# Dataset status
if 'df' in st.session_state and st.session_state['df'] is not None:
    df = st.session_state['df']
    st.subheader("📊 Current Dataset")
    st.write(f"Rows: {len(df)} | Columns: {len(df.columns)} | Memory: {df.memory_usage(deep=True).sum() / 1e6:.2f} MB")
    st.write(f"Numerical: {len(df.select_dtypes(include='number').columns)} | Categorical: {len(df.select_dtypes(include='object').columns)}")

    st.dataframe(df.head())

# Show recent actions
if 'code_log' in st.session_state and len(st.session_state['code_log']) > 1:
    st.subheader("📝 Recent Actions")
    st.code("\n".join(st.session_state['code_log'][1:]), language="python")

# Feature overview
st.subheader("🛠️ Features by Module")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Data Preparation**
    - 📁 Load CSV/Excel/JSON
    - 🔍 EDA Report
    - 🧹 Clean & Transform
    """)

with col2:
    st.markdown("""
    **Statistical Analysis**
    - 📊 Distribution Inspector
    - 📈 Residual Plots
    - 🔬 Normality Tests
    - 🎯 Feature vs Target Analysis
    """)

st.markdown("---")
st.markdown("Built with ❤️ using **Streamlit**, **Pandas**, and **Statsmodels**.")