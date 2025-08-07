🚀 MyDataTool: Interactive Data Exploration & Preprocessing App
A modular, user-friendly data analysis tool built with Streamlit and a custom Python package (datatools). This app helps you load, explore, clean, and visualize datasets interactively — ideal for EDA, teaching, or rapid prototyping.

✨ No coding required — just upload your data and go!
🧠 Every transformation is logged as executable Python code.
📊 Visualize distributions, linearity, and feature-target relationships in one place.

🧰 Features
This app includes the following interactive modules:

Section	Description
📁 Load Data	Upload CSV, Excel, or JSON files
🔍 Explore Data	Auto-generated EDA report with alerts for missing values, imbalances, etc.
🧹 Clean Data	Drop columns, handle missing values, remove duplicates, handle infinite values (inf, -inf)
📊 Analyze Distributions	Visualize distributions (histogram, KDE, boxplot, QQ plot) and view stats (skewness, kurtosis)
🎯 Feature vs Target	Interactive scatter and bar plots showing how features relate to the target variable
📈 Check Linearity	Residual plots to assess linearity for regression modeling
✅ All transformations are logged and exportable as Python code
✅ Built-in session reset and PDF report generation
✅ Modular design: core logic in a reusable datatools library

🛠️ Tech Stack
Frontend: Streamlit (interactive web app)
Core Logic: Custom datatools Python package
Visualization: Plotly, Seaborn, Matplotlib
Analysis: Pandas, NumPy, SciPy, StatsModels
Deployment: Streamlit Community Cloud