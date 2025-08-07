# datatools/analyzer.py
"""
Comprehensive module for statistical analysis and visualization.
Includes distribution inspection, normality tests and linearity checks.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from typing import Dict, Tuple, List, Optional
import warnings

def generate_column_info(df: pd.DataFrame, thresh_na: float = 0.25, thresh_balance: float = 0.5) -> pd.DataFrame:
    """Generate detailed EDA report per column."""
    info = pd.DataFrame(index=df.columns, columns=[
        'Dtype', 'Missing values (nb)', 'Missing values (%)',
        'Unique values (nb)', 'Unique values (list)',
        'Most common value', 'Alerts'
    ])

    info['Dtype'] = df.dtypes.values
    info['Missing values (nb)'] = df.isna().sum()
    info['Missing values (%)'] = df.isna().sum() / len(df) * 100
    info['Unique values (nb)'] = df.nunique()

    def get_unique_list(col):
        if col.nunique() > 10:
            return 'Lots of categories or values'
        else:
            return str(list(col.unique()))

    def get_mode(col):
        try:
            mode_val = col.mode()[0]
            return mode_val if not pd.isna(mode_val) else 'NaN'
        except:
            return 'N/A'

    def alerts(col):
        if (col.isna().sum() / len(df)) > thresh_na:
            return 'Lots of missing items'
        elif len(col) > 0 and col.value_counts(normalize=True).values[0] > thresh_balance:
            return 'Imbalanced data'
        else:
            return 'Looks fine'

    info['Unique values (list)'] = df.apply(get_unique_list)
    info['Most common value'] = df.apply(get_mode)
    info['Alerts'] = df.apply(alerts)

    return info

def summarize_dataset(df: pd.DataFrame) -> Dict[str, np.number]:
    total_cells = df.size
    missing = df.isna().sum().sum()
    return {
        'rows': len(df),
        'columns': len(df.columns),
        'total missing values': missing,
        'missing percentage': round((missing / total_cells) * 100, 2),
        'duplicates': df.duplicated().sum(),
        'numerical columns': len(df.select_dtypes(include='number').columns),
        'categorical columns': len(df.select_dtypes(include=['object', 'category']).columns),
        'other types': len(df.dtypes) - len(df.select_dtypes(include=['number', 'object', 'category']).columns),
        'total memory': df.memory_usage(deep=True).sum()


    }

def analyze_distribution(df: pd.DataFrame, columns: List[str]) -> Dict[str, pd.Series]:
    """Compute summary stats for numerical columns."""
    results = {}
    for col in columns:
        if col not in df.columns:
            warnings.warn(f"Column '{col}' not found.")
            continue
        if not pd.api.types.is_numeric_dtype(df[col]):
            warnings.warn(f"Column '{col}' is not numeric. Skipping.")
            continue

        series = df[col].dropna()
        results[col] = pd.Series({
            'mean': series.mean(),
            'median': series.median(),
            'std': series.std(),
            'skewness': series.skew(),
            'kurtosis': series.kurt(),
            'min': series.min(),
            'max': series.max(),
            'q25': series.quantile(0.25),
            'q75': series.quantile(0.75)
        })
    return results


def test_normality(df: pd.DataFrame, column: str, method: str = 'shapiro') -> Dict[str, float]:
    """Perform normality test on a single column."""
    data = df[column].dropna()
    if len(data) < 3:
        return {'error': 'Not enough data points'}

    if method == 'shapiro':
        if len(data) > 5000:
            return {'error': 'Shapiro-Wilk test only supports up to 5000 samples'}
        stat, p = stats.shapiro(data)
    elif method == 'kstest':
        stat, p = stats.kstest(data, 'norm')
    elif method == 'anderson':
        result = stats.anderson(data, dist='norm')
        return {
            'test_statistic': result.statistic,
            'critical_values': result.critical_values.tolist(),
            'significance_levels': result.significance_level.tolist()
        }
    else:
        return {'error': 'Unsupported method'}

    return {'statistic': stat, 'p_value': p}


def check_linearity_residuals(df: pd.DataFrame, target: str, feature: str) -> Tuple[np.ndarray, np.ndarray]:
    """Fit linear model and return fitted values and residuals."""
    data = df[[feature, target]].dropna()
    X = data[feature].values.reshape(-1, 1)
    y = data[target].values

    model = sm.OLS(y, sm.add_constant(X)).fit()
    y_pred = model.predict(sm.add_constant(X))
    residuals = y - y_pred

    return y_pred, residuals
