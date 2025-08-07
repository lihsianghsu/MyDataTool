# datatools/cleaner.py
import pandas as pd
import re
import numpy as np
from typing import List, Dict, Tuple
import warnings


def drop_columns(df, cols):
    return df.drop(columns=cols)

def fill_missing(df: pd.DataFrame, method: str = 'mean', custom_value=None) -> pd.DataFrame:
    """
    Fill missing values in DataFrame using various methods.
    
    Args:
        df: Input DataFrame
        method: Method to use ('mean', 'median', 'mode', 'ffill', 'bfill', 'custom')
        custom_value: Value to use when method='custom'
        
    Returns:
        DataFrame with missing values filled
    """
    df_filled = df.copy()
    
    if method == 'mean':
        # Fill numeric columns with mean
        numeric_cols = df_filled.select_dtypes(include=[np.number]).columns
        df_filled[numeric_cols] = df_filled[numeric_cols].fillna(df_filled[numeric_cols].mean())
        
    elif method == 'median':
        # Fill numeric columns with median
        numeric_cols = df_filled.select_dtypes(include=[np.number]).columns
        df_filled[numeric_cols] = df_filled[numeric_cols].fillna(df_filled[numeric_cols].median())
        
    elif method == 'mode':
        # Fill all columns with mode
        for col in df_filled.columns:
            mode_value = df_filled[col].mode()
            if not mode_value.empty:
                df_filled[col] = df_filled[col].fillna(mode_value[0])
                
    elif method == 'ffill':
        # Forward fill
        df_filled = df_filled.fillna(method='ffill')
        
    elif method == 'bfill':
        # Backward fill
        df_filled = df_filled.fillna(method='bfill')
        
    elif method == 'custom':
        # Fill with custom value
        df_filled = df_filled.fillna(value=custom_value)  # Note: use 'value' parameter
        
    return df_filled

def remove_duplicates(df):
    return df.drop_duplicates()

def convert_type(df: pd.DataFrame, col: str, dtype: str):
    df[col] = df[col].astype(dtype)
    return df

def handle_inf_values(
    df: pd.DataFrame,
    convert_to_nan: bool = True,
    log_inf_locations: bool = False
) -> pd.DataFrame:
    """
    Handle infinite values (inf, -inf) in the DataFrame.

    Args:
        df: Input DataFrame
        convert_to_nan: If True, replace inf with NaN. If False, cap with max/min finite values.
        log_inf_locations: If True, print locations (row, col) of infinite values.

    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    df = df.copy()

    # Find infinite values
    inf_mask = np.isinf(df.select_dtypes(include=[np.number]))
    num_inf = inf_mask.sum().sum()

    if num_inf == 0:
        if log_inf_locations:
            print("No infinite values found.")
        return df

    if log_inf_locations:
        inf_locations = df[inf_mask.any(axis=1)].index[inf_mask.any(axis=1)]
        print(f"Infinite values found in rows: {inf_locations.tolist()}")

    # Replace based on strategy
    if convert_to_nan:
        df = df.replace([np.inf, -np.inf], np.nan)
        if log_inf_locations:
            print(f"Replaced {num_inf} infinite values with NaN.")
    else:
        # Cap with finite max/min
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if inf_mask[col].any():
                finite_max = df[col].replace([np.inf, -np.inf], np.nan).max()
                finite_min = df[col].replace([np.inf, -np.inf], np.nan).min()
                df[col] = df[col].replace(np.inf, finite_max)
                df[col] = df[col].replace(-np.inf, finite_min)

    return df

def clean_column_names(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, str], Dict[str, str]]:
    """Clean column names to be valid Python identifiers and avoid formula errors."""
    column_mapping = {}
    used_names = set()

    for i, col in enumerate(df.columns):
        name = re.sub(r'\W+', '_', str(col).strip())
        name = f'_{name}' if name and name[0].isdigit() else name or f'col_{i}'

        # Ensure uniqueness
        base = name
        counter = 1
        while name in used_names:
            name = f"{base}_{counter}"
            counter += 1

        column_mapping[col] = name
        used_names.add(name)

    df_clean = df.copy()
    df_clean.columns = list(column_mapping.values())
    reverse_mapping = {v: k for k, v in column_mapping.items()}

    return df_clean, column_mapping, reverse_mapping


def is_suitable_categorical(series: pd.Series, max_unique_ratio: float = 0.05, max_unique_count: int = 20) -> bool:
    """Check if a series is suitable for categorical analysis."""
    if series.empty or series.dropna().empty:
        return False

    if not pd.api.types.is_numeric_dtype(series):
        return True

    unique_count = series.nunique(dropna=True)
    unique_ratio = unique_count / len(series.dropna())

    return unique_count <= max_unique_count or unique_ratio <= max_unique_ratio


def get_categorical_columns(df: pd.DataFrame, exclude: List[str] = []) -> List[str]:
    """Return column names suitable for categorical analysis, excluding specified ones."""
    return [
        col for col in df.columns
        if col not in exclude and is_suitable_categorical(df[col])
    ]


def prepare_dataframe_for_analysis(df: pd.DataFrame, target: str = None) -> pd.DataFrame:
    """Remove empty columns and rows where target is missing."""
    df_clean = df.dropna(axis=1, how='all')
    if target and target in df_clean.columns:
        df_clean = df_clean.dropna(subset=[target])
    return df_clean


def clean_dataframe_comprehensive(df: pd.DataFrame) -> pd.DataFrame:
    """Drop empty rows/columns and ensure column name uniqueness."""
    df_clean = df.dropna(how='all').dropna(axis=1, how='all')

    if df_clean.columns.duplicated().any():
        cols = pd.Series(df_clean.columns)
        for dup in cols[cols.duplicated()].unique():
            dup_indices = cols[cols == dup].index
            cols.loc[dup_indices] = [f"{dup}_{i}" if i else dup for i in range(len(dup_indices))]
        df_clean.columns = cols

    return df_clean


__all__ = [
    'drop_columns',
    'fill_missing',
    'remove_duplicates',
    'convert_type',
    'handle_inf_values',
    'clean_column_names',
    'is_suitable_categorical',
    'get_categorical_columns',
    'prepare_dataframe_for_analysis',
    'clean_dataframe_comprehensive'
]