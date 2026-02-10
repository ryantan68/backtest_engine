import pandas as pd
import numpy as np
from scipy.stats import norm
import copy

def generate_polynomial(ticker):

    df = pd.read_excel(rf"C:\Users\ryant\OneDrive\Desktop\Options Pricing Analysis\Refined Vol Surfaces\{ticker}_vol_surface_refined.xlsx")

    for i in range(5):
        df[f"function_{i+1}"] = pd.Series([None]*len(df), dtype='object')

    for i in range(len(df)):
        for j in range(5):
    
            df[f"DTE_{j+1}"].astype(float)
            base_val = df.loc[i, f"base_val_{j+1}"]
            atm_vol = df.loc[i, f"atm_vol_{j+1}"]
            dte = df.loc[i, f"DTE_{j+1}"]

            d0 = df.loc[i, f"d0_{j+1}"]
            d1 = df.loc[i, f"d1_{j+1}"]
            d2 = df.loc[i, f"d2_{j+1}"]
            u0 = df.loc[i, f"u0_{j+1}"]
            u1 = df.loc[i, f"u1_{j+1}"]
            u2 = df.loc[i, f"u2_{j+1}"]

            x1 = base_val - base_val * 2 * (atm_vol/100) * (dte/365)**0.5
            x2 = base_val - base_val * 1 * (atm_vol/100) * (dte/365)**0.5
            x3 = base_val - base_val * 0.5 * (atm_vol/100) * (dte/365)**0.5
            x4 = base_val
            x5 = base_val + base_val * 0.5 * (atm_vol/100) * (dte/365)**0.5
            x6 = base_val + base_val * 1 * (atm_vol/100) * (dte/365)**0.5
            x7 = base_val + base_val * 2 * (atm_vol/100) * (dte/365)**0.5

            y1 = atm_vol + d2
            y2 = atm_vol + d1
            y3 = atm_vol + d0
            y4 = atm_vol
            y5 = atm_vol + u0
            y6 = atm_vol + u1
            y7 = atm_vol + u2

            x = np.array([x1, x2, x3, x4, x5, x6, x7], dtype=float)
            y = np.array([y1, y2, y3, y4, y5, y6, y7], dtype=float)

            deg = 5
            coeffs = np.polyfit(x, y, deg=deg)
            poly_func = np.poly1d(coeffs)
            poly_str = " + ".join(f"{c}*x**{k}" for k, c in enumerate(reversed(coeffs)))
            
            df.at[i, f"function_{j+1}"] = poly_func
            df.loc[i, f"equation_{j+1}"] = poly_str

    df["positions"] = pd.Series([None]*len(df), dtype='object')
    df["positions_value"] = pd.Series([None]*len(df), dtype='object')
    df["prev_positions"] = pd.Series([None]*len(df), dtype='object')
    df["prev_positions_value"] = pd.Series([None]*len(df), dtype='object')

    return df

def calculate_pnl(df):

    for i in range(1, len(df)):

        df.at[i, "prev_positions"] = df.loc[i-1, "positions"]

    for i in range(1, len(df)-1):

        positions_copy = copy.deepcopy(df.loc[i, "positions"])

        for pos in positions_copy:

            expiry_number = pos["expiry"]
            base = df.loc[i, f"base_val_{expiry_number}"]
            strike = pos["strike"]
            dte = df.loc[i, f"DTE_{expiry_number}"]
            implied_vol = df.loc[i, f"function_{expiry_number}"](strike)
            option_type = pos["option_type"]
            
            pos["price"] = black_scholes_inverse(base,
                                                strike,
                                                dte/365,
                                                0,
                                                implied_vol/100,
                                                option_type
                                                )
        
        df.at[i, "positions_value"] = positions_copy

    for i in range(1, len(df)):

        prev_positions_copy = copy.deepcopy(df.loc[i, "prev_positions"])

        for pos in prev_positions_copy:

            expiry_number = pos["expiry"]
            base = df.loc[i, f"base_val_{expiry_number}"]
            strike = pos["strike"]
            dte = df.loc[i, f"DTE_{expiry_number}"]
            implied_vol = df.loc[i, f"function_{expiry_number}"](strike)
            option_type = pos["option_type"]
            
            pos["price"] = black_scholes_inverse(base,
                                                strike,
                                                dte/365,
                                                0,
                                                implied_vol/100,
                                                option_type
                                                )
        
        df.at[i, "prev_positions_value"] = prev_positions_copy

    df["PnL"] = 0

    for i in range(2, len(df)):

        pnl = 0

        before = copy.deepcopy(df.loc[i-1, "positions_value"])
        after = copy.deepcopy(df.loc[i, "prev_positions_value"])

        for pos1, pos2 in zip(before, after):

            contract_pnl = (pos2["price"] - pos1["price"]) * pos1["size"]
            pnl += contract_pnl
        
        df.loc[i, "PnL"] = pnl

    df["Cumulative PnL"] = df["PnL"].cumsum()

    return df

def black_scholes_inverse(S, K, T, r, sigma, option_type):

    # Call Option

    d1_call = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2_call = d1_call - sigma * np.sqrt(T)
    call_price = S * norm.cdf(d1_call) - K * np.exp(-r * T) * norm.cdf(d2_call)

    # Put Option

    d1_put = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2_put = d1_put - sigma * np.sqrt(T)
    put_price = K * np.exp(-r * T) * norm.cdf(-d2_put) - S * norm.cdf(-d1_put)

    if option_type == "call":
        price = call_price
    elif option_type == "put":
        price = put_price

    return float(price)

# to merge and split the dfs for multi asset strategies

def merge_dataframes(df1, df2, date_col="date", suffix1="_A", suffix2="_B"):
    """
    Merges two DataFrames with identical columns on a date column.
    
    Parameters:
        df1: First DataFrame (e.g., SPX)
        df2: Second DataFrame (e.g., NDX)
        date_col: Name of the date column to merge on
        suffix1: Suffix for df1 columns
        suffix2: Suffix for df2 columns
    
    Returns:
        Merged DataFrame
    """
    df_merged = pd.merge(
        df1, 
        df2, 
        on=date_col, 
        suffixes=(suffix1, suffix2),
        how="inner"
    )
    
    return df_merged


def split_dataframe(df_merged, date_col="date", suffix1="_A", suffix2="_B"):
    """
    Splits a merged DataFrame back into two separate DataFrames.
    Non-suffixed columns (except date) are included in both DataFrames.

    Parameters:
        df_merged: The merged DataFrame
        date_col: Name of the date column
        suffix1: Suffix for first DataFrame columns
        suffix2: Suffix for second DataFrame columns

    Returns:
        df1, df2: Two separate DataFrames with original column names
    """
    # Find columns that don't have either suffix (shared/new columns)
    shared_cols = [col for col in df_merged.columns
                   if not col.endswith(suffix1)
                   and not col.endswith(suffix2)
                   and col != date_col]

    cols_df1 = [date_col] + [col for col in df_merged.columns if col.endswith(suffix1)] + shared_cols
    cols_df2 = [date_col] + [col for col in df_merged.columns if col.endswith(suffix2)] + shared_cols

    df1 = df_merged[cols_df1].copy()
    df2 = df_merged[cols_df2].copy()

    df1.columns = [col.replace(suffix1, "") if col.endswith(suffix1) else col for col in df1.columns]
    df2.columns = [col.replace(suffix2, "") if col.endswith(suffix2) else col for col in df2.columns]

    return df1, df2