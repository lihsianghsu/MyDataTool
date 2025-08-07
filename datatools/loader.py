# loader.py
import pandas as pd

def load_dataframe(file, filetype='csv', sep=','):
    if filetype == 'csv':
        return pd.read_csv(file, sep=sep)
    elif filetype == 'excel' or filetype == 'xlsx':
        return pd.read_excel(file)
    elif filetype == 'json':
        return pd.read_json(file)
    else:
        raise ValueError("Unsupported file type")