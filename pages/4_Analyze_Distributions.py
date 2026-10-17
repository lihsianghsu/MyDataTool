# pages/4_Analyze_Distributions.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import plotly.express as px
import plotly.figure_factory as ff

st.header("📊 Analyze Distributions")
st.markdown("Select features and visualize their distributions.")

if 'df' in st.session_state:
    df = st.session_state['df']

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    selected_cols = st.multiselect("Select one or more features", options=numeric_cols)

    if selected_cols:
        plot_type = st.selectbox("Select plot type", [
            "Histogram",
            "Line Plot",
            "KDE Plot",
            "Histogram + KDE",
            "ECDF Plot",
            "Boxplot",
            "Violin Plot",
            "Boxen Plot",
            #"Swarm Plot",
            "Rug Plot",
            "QQ Plot",
            "Pairwise Distribution"
        ])

        if plot_type == "Histogram":
            for col in selected_cols:
                fig = px.histogram(df, x=col, title=f"Histogram of {col}")
                st.plotly_chart(fig)
                
        elif plot_type == "Line Plot":
            for col in selected_cols:
                sorted_values = df[col].dropna().sort_values().reset_index(drop=True)
        
                plt.figure(figsize=(8, 4))
                sns.lineplot(x=range(len(sorted_values)), y=sorted_values)
                plt.title(f"Line Plot of {col}")
                plt.xlabel("Observation (sorted)")
                plt.ylabel(col)
                st.pyplot(plt)
                plt.clf()

        elif plot_type == "KDE Plot":
            for col in selected_cols:
                fig = sns.kdeplot(df[col])
                plt.title(f"KDE Plot of {col}")
                st.pyplot(plt)
                plt.clf()

        elif plot_type == "Histogram + KDE":
            for col in selected_cols:
                plt.figure(figsize=(8, 4))
                sns.histplot(df[col], kde=True)
                plt.title(f"Histogram + KDE of {col}")
                st.pyplot(plt)
                plt.clf()        
                
        elif plot_type == "ECDF Plot":
            for col in selected_cols:
                fig = sns.ecdfplot(df[col])
                plt.title(f"ECDF Plot of {col}")
                st.pyplot(plt)
                plt.clf()

        elif plot_type == "Boxplot":
            for col in selected_cols:
                fig = px.box(df, y=col, title=f"Boxplot of {col}")
                st.plotly_chart(fig)
                
        elif plot_type == "Violin Plot":
            for col in selected_cols:
                plt.figure(figsize=(8, 3))
                sns.violinplot(x=df[col])
                plt.title(f"Violin Plot of {col}")
                st.pyplot(plt)
                plt.clf()
                
        elif plot_type == "Boxen Plot":
            for col in selected_cols:
                plt.figure(figsize=(8, 2))
                sns.boxenplot(x=df[col])
                plt.title(f"Boxen Plot of {col}")
                st.pyplot(plt)
                plt.clf()
                
        elif plot_type == "QQ Plot":
            for col in selected_cols:
                fig = stats.probplot(df[col], dist="norm", plot=plt)
                plt.title(f"QQ Plot of {col}")
                st.pyplot(plt)
                plt.clf()

        elif plot_type == "Rug Plot":
            for col in selected_cols:
                plt.figure(figsize=(8, 2))
                sns.rugplot(x=df[col])
                plt.title(f"Rug Plot of {col}")
                st.pyplot(plt)
                plt.clf()  
                
        elif plot_type == "Swarm Plot":
            for col in selected_cols:
                plt.figure(figsize=(10, 3))
                sns.swarmplot(x=df[col], size=3)
                plt.title(f"Swarm Plot of {col}")
                st.pyplot(plt)
                plt.clf()
                
        elif plot_type == "Pairwise Distribution":
            fig = sns.pairplot(df[selected_cols])
            st.pyplot(fig)

        # Show summary stats
        st.subheader("📊 Summary Statistics")
        stats_df = df[selected_cols].agg(['mean', 'median', 'std', 'skew']).T
        st.dataframe(stats_df)

else:
    st.warning("Please upload a dataset in the 'Load Data' tab first.")
