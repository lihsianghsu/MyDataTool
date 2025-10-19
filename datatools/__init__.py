# datatools/__init__.py
"""
datatools: A lightweight toolkit for EDA, cleaning, and statistical analysis.
"""
from .loader import load_dataframe
from .cleaner import (
    drop_columns,
    fill_missing,
    remove_duplicates,
    handle_inf_values,
    convert_type
)
from .analyzer import (
    generate_column_info,
    summarize_dataset,
    analyze_distribution,
    test_normality,
    check_linearity_residuals
)
from .utils import (
    is_numeric_series,
    list_numeric_columns,
    list_categorical_columns,
    validate_column_in_df
)

__version__ = "0.1.0"
__author__ = "Li-Hsiang Hsu"

__all__ = [
    # Loader
    "load_dataframe",
    # Cleaner
    "drop_columns",
    "fill_missing",
    "remove_duplicates",
    "convert_type",
    "clean_column_names",
    "prepare_dataframe_for_analysis",
    "clean_dataframe_comprehensive",
    "is_suitable_categorical",
    "get_categorical_columns",
    "handle_inf_values",
    # Analyzer
    "generate_column_info",
    "summarize_dataset",
    "analyze_distribution",
    "test_normality",
    "check_linearity_residuals",
    # Utils
    "is_numeric_series",
    "list_numeric_columns",
    "list_categorical_columns",
    "validate_column_in_df"
]
