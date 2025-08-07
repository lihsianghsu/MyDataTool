# pages/6_Check_Linearity.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

st.header("📈 Check Linearity")
st.markdown("Use residual plots to assess linearity between features and a target variable.")

if 'df' in st.session_state:
    df = st.session_state['df']

    numeric_cols = df.select_dtypes(include=['int', 'float']).columns.tolist()
    target = st.selectbox("Select target variable", options=numeric_cols)

    if target:
        X_cols = st.multiselect("Select predictor(s)", options=[c for c in numeric_cols if c != target])

        if X_cols:
            # Fit model and plot residuals
            for x in X_cols:
                st.subheader(f"Residual Plot: {x} → {target}")

                # Drop NaNs
                data = df[[x, target]].dropna()

                # Fit linear regression
                model = LinearRegression()
                X = data[x].values.reshape(-1, 1)
                y = data[target].values
                model.fit(X, y)
                y_pred = model.predict(X)
                residuals = y - y_pred

                # Plot residuals
                fig, ax = plt.subplots(figsize=(6, 4))
                sns.residplot(x=y_pred, y=residuals, lowess=True, ax=ax, color='blue')
                ax.set_xlabel("Fitted Values")
                ax.set_ylabel("Residuals")
                ax.set_title(f"Residual Plot for {x}")
                ax.axhline(0, color='red', linestyle='--')
                st.pyplot(fig)

                # Metrics
                r2 = model.score(X, y)
                rmse = np.sqrt(np.mean(residuals**2))
                st.caption(f"R²: {r2:.3f} | RMSE: {rmse:.3f}")

                # Interpretation
                #if abs(residuals.mean()) < 0.1 * np.std(residuals):
                #    st.success("Residuals appear randomly scattered – linearity likely holds.")
                #else:
                #    st.warning("Pattern in residuals – possible non-linearity detected.")

else:
    st.warning("Please upload a dataset in the 'Load Data' tab first.")