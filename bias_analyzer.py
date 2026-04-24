import pandas as pd

def compute_selection_rate(data):
    df = pd.DataFrame(data)
    return df.groupby("group")["selected"].mean()

def demographic_parity(data):
    rates = compute_selection_rate(data)
    return rates.max() - rates.min()