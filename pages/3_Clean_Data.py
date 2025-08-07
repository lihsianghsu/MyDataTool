# pages/3_Clean_Data.py
import streamlit as st
import pandas as pd
import numpy as np

# Import from core library
from datatools.cleaner import drop_columns, fill_missing, remove_duplicates, handle_inf_values
from datatools.utils import log_code, list_numeric_columns, list_categorical_columns

st.header("🧹 Clean Data")
st.markdown("Apply common data cleaning steps interactively. All actions are logged for reproducibility.")

# Check if data is loaded
if 'df' not in st.session_state or st.session_state['df'] is None:
    st.warning("Please upload a dataset in the 'Load Data' tab first.")
    st.stop()

df = st.session_state['df'].copy()

# Keep a flag to track if any change was made
changes_made = False

# ===========================
# Drop Columns
# ===========================
st.subheader("🗑️ Drop Columns")
cols_to_drop = st.multiselect(
    "Select columns to drop",
    options=df.columns.tolist(),
    help="Choose one or more columns to remove from the dataset."
)

if cols_to_drop:
    if st.button("Apply: Drop Selected Columns"):
        df = drop_columns(df, cols_to_drop)
        st.session_state['df'] = df
        log_code(f"df = df.drop(columns={cols_to_drop})")
        st.success(f"✅ Dropped columns: `{', '.join(cols_to_drop)}`")
        changes_made = True

# ===========================
# Handle Missing Values
# ===========================
st.subheader("🔄 Handling Missing Values")

# Method selection
missing_method = st.selectbox(
    "Choose method to handle missing values",
    options=["None", "Mean (numeric)", "Median (numeric)", "Mode (all)", 
             "Forward Fill", "Backward Fill", "Custom Value"],
    help="Select how to fill NaN values in the dataset."
)

# Safety check
if missing_method == "Mode (all)":
    for col in df.columns:
        mode_vals = df[col].mode()
        if len(mode_vals) == 0:
            st.warning(f"⚠️ Column '{col}' has no mode (all values missing?). Will skip.")

# Custom value input (only show when needed)
custom_value = None
if missing_method == "Custom Value":
    custom_value = st.text_input("Enter custom value:", value="0")

# Apply button
if st.button(f"Apply: Fill Missing with {missing_method}") and missing_method != "None":
    # Map methods to internal names
    method_map = {
        "Mean (numeric)": "mean",
        "Median (numeric)": "median", 
        "Mode (all)": "mode",
        "Forward Fill": "ffill",
        "Backward Fill": "bfill",
        "Custom Value": "custom"
    }
    
    method = method_map.get(missing_method)
    
    if method:
        try:
            # Handle custom value conversion
            if missing_method == "Custom Value" and custom_value is not None:
                # Try to convert to appropriate type
                if custom_value.lower() in ['true', 'false']:
                    custom_value = custom_value.lower() == 'true'
                else:
                    try:
                        # Try integer first
                        if '.' not in custom_value and custom_value.lstrip('-').isdigit():
                            custom_value = int(custom_value)
                        else:
                            custom_value = float(custom_value)
                    except ValueError:
                        # Keep as string if not numeric
                        if custom_value.lower() in ['none', 'null', 'nan']:
                            custom_value = None
                        # Remove quotes if user added them
                        custom_value = custom_value.strip('"\'')
            
            # Apply the missing value filling
            df_filled = fill_missing(df, method=method, custom_value=custom_value)
            st.session_state['df'] = df_filled
            
            # Success message
            if missing_method == "Custom Value":
                st.success(f"✅ Missing values filled with custom value: {custom_value}")
            else:
                st.success(f"✅ Missing values filled using `{missing_method}`.")
                
            changes_made = True
            
        except Exception as e:
            st.error(f"Error applying missing value method: {str(e)}")

# ===========================
# Detect and Handle Inf Values
# ===========================
st.subheader("⚠️ Handle Infinite Values")
st.markdown("""
Detect and handle `inf` or `-inf` values (common after log transformations or division).
""")

# Check for infinite values
has_inf = np.isinf(df.select_dtypes(include=[np.number])).any().any()

if has_inf:
    st.warning("⚠️ Infinite values (`inf`, `-inf`) detected in numerical columns.")

    inf_action = st.radio(
        "How would you like to handle infinite values?",
        options=[
            "Replace with NaN",
            "Cap with max/min finite values",
            "Skip for now"
        ],
        help="Choose how to treat infinite values before further processing."
    )

    if st.button("Apply: Handle Infinite Values"):
        if inf_action == "Replace with NaN":
            df = handle_inf_values(df, convert_to_nan=True, log_inf_locations=True)
            log_code("df = df.replace([np.inf, -np.inf], np.nan)")
            st.success("✅ Replaced `inf` and `-inf` with `NaN`.")
            changes_made = True

        elif inf_action == "Cap with max/min finite values":
            df = handle_inf_values(df, convert_to_nan=False, log_inf_locations=True)
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if np.isinf(df[col]).any():
                    finite_max = df[col].replace([np.inf, -np.inf], np.nan).max()
                    finite_min = df[col].replace([np.inf, -np.inf], np.nan).min()
                    log_code(f"# Capped inf values in '{col}' with finite max={finite_max:.2f}, min={finite_min:.2f}")
            st.success("✅ Capped `inf` and `-inf` with finite max/min values.")
            changes_made = True

else:
    st.success("✅ No infinite values found in numerical columns.")
    inf_action = "Skip for now"  # For downstream logic

# Save state
if changes_made:
    st.session_state['df'] = df


# ===========================
# Remove Duplicates
# ===========================
st.subheader("🧼 Remove Duplicate Rows")
if st.checkbox("Preview duplicates", help="Show how many duplicate rows exist"):
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        st.info(f"Found {dup_count} duplicate row(s).")
    else:
        st.success("No duplicates found.")

if st.button("Remove All Duplicates"):
    original_count = len(df)
    df = remove_duplicates(df)
    new_count = len(df)
    st.session_state['df'] = df

    log_code("df = df.drop_duplicates()")
    st.success(f"✅ Removed {original_count - new_count} duplicate(s). Dataset now has {new_count} rows.")
    changes_made = True
# ===========================
# Clean Column Names
# ===========================
#st.subheader("🧽 Clean Column Names")

# ===========================
# Preview Updated DataFrame
# ===========================
st.subheader("📋 Preview Processed DataFrame")
st.dataframe(df.head())

# Show shape info
st.caption(f"Current shape: {df.shape[0]} rows × {df.shape[1]} columns")

# ===========================
# Reset to Original Data
# ===========================
st.divider()
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Reset to Original Data"):
        st.session_state['df'] = st.session_state['df_raw'].copy()
        log_code("# Reset to original loaded data")
        st.success("DataFrame reset to original state.")
        st.rerun()

with col2:
    if st.button("🧹 Clear All Changes"):
        st.session_state['df'] = st.session_state['df_raw'].copy()
        st.success("All changes cleared.")
        st.rerun()

# ===========================
# Final Update to Session State
# ===========================
if changes_made:
    st.session_state['df'] = df  # Ensure latest df is saved