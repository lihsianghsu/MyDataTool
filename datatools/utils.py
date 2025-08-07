"""
Utility functions for both data processing and Streamlit UI interactions.

This module contains:
- Core data helpers (column listing, validation)
- Streamlit-specific tools (code logging, session reset)
"""

import streamlit as st
import pandas as pd
from typing import List, Optional, Any

# =============================================================================
# 🔧 DATA UTILITIES
# =============================================================================

def is_numeric_series(series: pd.Series) -> bool:
    """Check if a pandas Series has a numeric dtype."""
    return pd.api.types.is_numeric_dtype(series)


def list_numeric_columns(df: pd.DataFrame) -> List[str]:
    """Return list of numeric column names."""
    return df.select_dtypes(include='number').columns.tolist()


def list_categorical_columns(df: pd.DataFrame) -> List[str]:
    """Return list of categorical (object/category) column names."""
    return df.select_dtypes(include=['object', 'category']).columns.tolist()


def validate_column_in_df(df: pd.DataFrame, col: str, raise_error: bool = True) -> bool:
    """
    Validate that a column exists in the DataFrame.

    Args:
        df: Input DataFrame
        col: Column name to check
        raise_error: Whether to raise ValueError if not found

    Returns:
        True if column exists, False otherwise
    """
    if col not in df.columns:
        if raise_error:
            raise ValueError(f"Column '{col}' not found in DataFrame with columns: {list(df.columns)}")
        return False
    return True


def get_sample_values(series: pd.Series, n: int = 5) -> List[Any]:
    """
    Get up to n non-null sample values from a series.

    Args:
        series: Input pandas Series
        n: Number of samples to return

    Returns:
        List of sample values
    """
    return series.dropna().head(n).tolist()


def safe_dropna(series: pd.Series) -> pd.Series:
    """Drop NA values safely."""
    return series.dropna()


# =============================================================================
# 🖥️ STREAMLIT UI UTILITIES
# =============================================================================

def log_code(code_line: str) -> None:
    """
    Append a line of executable Python code to the session state log.

    This enables a "code export" feature in the Streamlit app,
    showing users exactly what transformations were applied.

    Args:
        code_line: A string containing valid Python code (e.g., "df = df.drop(columns=['age'])")
    """
    if 'code_log' not in st.session_state:
        st.session_state['code_log'] = ["# Data Processing Log\n"]
    st.session_state['code_log'].append(code_line.strip())


def reset_session() -> None:
    """
    Reset the Streamlit session state to initial conditions.

    Clears:
        - 'df': Current working DataFrame
        - 'df_raw': Original loaded DataFrame
        - 'code_log': Logged transformation code

    Re-initializes code log for new session.
    """
    keys_to_clear = ['df', 'df_raw', 'code_log']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    # Re-init code log
    st.session_state['code_log'] = ["# New session started\n"]


def get_code_string() -> str:
    """
    Return the full logged code as a single string.

    Useful for displaying or downloading the transformation script.

    Returns:
        Multi-line string of Python code
    """
    return "\n".join(st.session_state.get('code_log', ['# No code logged']))


def download_code_button(filename: str = "data_processing_script.py") -> None:
    """
    Display a download button for the logged code in the sidebar.

    Args:
        filename: Name of the file to download (default: data_processing_script.py)
    """
    code = get_code_string()
    st.sidebar.download_button(
        label="📥 Download Code",
        data=code,
        file_name=filename,
        mime="text/x-python",
        key="download_code_btn"
    )


# =============================================================================
# 🛠️ MISC HELPERS
# =============================================================================

def print_if_debug(*args, debug: bool = False) -> None:
    """
    Conditional print for debugging.

    Args:
        *args: Values to print
        debug: If True, print the values
    """
    if debug:
        print("[DEBUG]", *args)


def is_empty_or_none(val: Any) -> bool:
    """Check if value is None, empty, or NaN."""
    if val is None:
        return True
    if isinstance(val, (str, list, dict, pd.Series, pd.DataFrame)) and len(val) == 0:
        return True
    if pd.isna(val):
        return True
    return False