# pages/8_Feature_vs_Target.py
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Import utilities
from datatools.utils import list_numeric_columns, list_categorical_columns, validate_column_in_df

st.header("🎯 Feature vs Target Analysis")
st.markdown("Visualize how each feature relates to the target variable.")

if 'df' not in st.session_state or st.session_state['df'] is None:
    st.warning("Please upload a dataset first.")
    st.stop()

df = st.session_state['df']

# Select target
target = st.selectbox(
    "Select the target variable (Y)",
    options=df.columns,
    index=df.columns.tolist().index('SalePrice') if 'SalePrice' in df.columns else 0
)

if not validate_column_in_df(df, target, raise_error=False):
    st.error("Target column not found.")
    st.stop()

# Check if target is numeric
if not np.issubdtype(df[target].dtype, np.number):
    st.warning(f"Target '{target}' is not numeric. Consider using ANOVA instead.")
    st.stop()

# ===========================
# Numerical Features vs Target
# ===========================
st.subheader("🔢 Numerical Features vs Target")
st.markdown(f"Scatter plots: `{target}` vs. numeric features")

numerical_cols = [col for col in list_numeric_columns(df) if col != target]

if numerical_cols:
    n_cols_grid = st.slider("Number of columns in grid", 2, 6, 5)
    n_rows = (len(numerical_cols) + n_cols_grid - 1) // n_cols_grid

    fig, axes = plt.subplots(n_rows, n_cols_grid, figsize=(4 * n_cols_grid, 4 * n_rows))
    axes = axes.flatten() if len(numerical_cols) > 1 else [axes]

    for i, col in enumerate(numerical_cols):
        sns.scatterplot(ax=axes[i], x=df[col], y=df[target], s=12, alpha=0.7)
        axes[i].set_title(f"{target} vs {col}", fontsize=10)
        axes[i].set_xlabel(col, fontsize=9)
        axes[i].set_ylabel(target, fontsize=9)
        axes[i].tick_params(axis='x', labelrotation=45, labelsize=8)

    # Hide unused subplots
    for i in range(len(numerical_cols), len(axes)):
        fig.delaxes(axes[i])

    plt.suptitle(f'{target} vs Numerical Features', fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    st.pyplot(fig)
else:
    st.info("No numerical features found (excluding target).")

# ===========================
# Categorical Features vs Target
# ===========================
st.subheader("🏷️ Categorical Features vs Target")
st.markdown(f"Bar plots: `{target}` vs. categorical features")

categorical_cols = list_categorical_columns(df)

if categorical_cols:
    n_cols_grid = st.slider("Number of columns in grid (categorical)", 2, 6, 4)
    n_rows = (len(categorical_cols) + n_cols_grid - 1) // n_cols_grid

    fig, axes = plt.subplots(n_rows, n_cols_grid, figsize=(4 * n_cols_grid, 4 * n_rows))
    axes = axes.flatten() if len(categorical_cols) > 1 else [axes]

    for i, col in enumerate(categorical_cols):
        # Sort categories by mean target value for better readability
        order = df.groupby(col)[target].mean().sort_values(ascending=False).index
        sns.barplot(ax=axes[i], x=df[col], y=df[target], order=order, palette="Blues_d")
        axes[i].set_title(f"{target} vs {col}", fontsize=10)
        axes[i].set_xlabel(col, fontsize=9)
        axes[i].set_ylabel(target, fontsize=9)
        axes[i].tick_params(axis='x', labelrotation=45, labelsize=8)

    # Hide unused subplots
    for i in range(len(categorical_cols), len(axes)):
        fig.delaxes(axes[i])

    plt.suptitle(f'{target} vs Categorical Features', fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    st.pyplot(fig)
else:
    st.info("No categorical features found.")

# ===========================
# Optional: Log this as analysis (not a transformation)
# ===========================
# No log_code() needed — this is exploratory, not transformative