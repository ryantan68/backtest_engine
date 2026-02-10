from greeks_hedge_ratio import *

# Standard Structures

def butterfly(df, expiry, sd, atm_qty, wings_qty):

    for i in range(len(df)-1):

        base_val = df.loc[i, f"base_val_{expiry}"]
        dte = df.loc[i, f"DTE_{expiry}"]
        atm_vol = df.loc[i, f"atm_vol_{expiry}"]/100

        if df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and df.loc[i+1, "base_change_1"] > -0.45:

            df.at[i,"positions"] = [{"strike":base_val*(1+sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "call", "size": wings_qty * 10},
                                    {"strike":base_val*(1-sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "put", "size": wings_qty * 10},
                                    {"strike":base_val, "expiry": expiry, "option_type": "call", "size": atm_qty * 10},
                                    {"strike":base_val, "expiry": expiry, "option_type": "put", "size": atm_qty * 10}]

        else:
            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": 0}]

    return df

def risk_reversal(df, expiry, sd, put_qty, call_qty):

    for i in range(len(df)-1):

        base_val = df.loc[i, f"base_val_{expiry}"]
        dte = df.loc[i, f"DTE_{expiry}"]
        atm_vol = df.loc[i, f"atm_vol_{expiry}"]/100

        if df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and df.loc[i+1, "base_change_1"] > -0.45:

            df.at[i,"positions"] = [{"strike":base_val*(1+sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "call", "size": call_qty * 10},
                                    {"strike":base_val*(1-sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "put", "size": put_qty * 10}]

        else:
            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": 0}]

    return df


def strangle_swap(df, expiry_1, expiry_2, sd):

    for i in range(len(df)-1):

        base_val_1 = df.loc[i, f"base_val_{expiry_1}"]
        base_val_2 = df.loc[i, f"base_val_{expiry_2}"]
        dte_1 = df.loc[i, f"DTE_{expiry_1}"]
        dte_2 = df.loc[i, f"DTE_{expiry_2}"]
        atm_vol_1 = df.loc[i, f"atm_vol_{expiry_1}"]/100
        atm_vol_2 = df.loc[i, f"atm_vol_{expiry_2}"]/100

        if df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and atm_vol_1 > atm_vol_2 and df.loc[i+1, "base_change_1"] > -0.45:

            df.at[i,"positions"] = [{"strike":base_val_1*(1+sd*atm_vol_1*((dte_1/365)**0.5)), "expiry": expiry_1, "option_type": "call", "size": -10},
                                    {"strike":base_val_1*(1-sd*atm_vol_1*((dte_1/365)**0.5)), "expiry": expiry_1, "option_type": "put", "size": -10},
                                    {"strike":base_val_2*(1+sd*atm_vol_2*((dte_2/365)**0.5)), "expiry": expiry_2, "option_type": "call", "size": 10},
                                    {"strike":base_val_2*(1-sd*atm_vol_2*((dte_2/365)**0.5)), "expiry": expiry_2, "option_type": "put", "size": 10}]

        elif df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and atm_vol_1 < atm_vol_2 and df.loc[i+1, "base_change_1"] > -0.45:

            df.at[i,"positions"] = [{"strike":base_val_1*(1+sd*atm_vol_1*((dte_1/365)**0.5)), "expiry": expiry_1, "option_type": "call", "size": 10},
                                    {"strike":base_val_1*(1-sd*atm_vol_1*((dte_1/365)**0.5)), "expiry": expiry_1, "option_type": "put", "size": 10},
                                    {"strike":base_val_2*(1+sd*atm_vol_2*((dte_2/365)**0.5)), "expiry": expiry_2, "option_type": "call", "size": -10},
                                    {"strike":base_val_2*(1-sd*atm_vol_2*((dte_2/365)**0.5)), "expiry": expiry_2, "option_type": "put", "size": -10}]
        else:
            df.at[i,"positions"] = [{"strike":base_val_1, "expiry": expiry_1, "option_type": "call", "size": 0}]

    return df

def risk_reversal_swap(df, expiry_1, expiry_2, sd):

    for i in range(len(df)-1):

        base_val_1 = df.loc[i, f"base_val_{expiry_1}"]
        base_val_2 = df.loc[i, f"base_val_{expiry_2}"]
        dte_1 = df.loc[i, f"DTE_{expiry_1}"]
        dte_2 = df.loc[i, f"DTE_{expiry_2}"]
        atm_vol_1 = df.loc[i, f"atm_vol_{expiry_1}"]/100
        atm_vol_2 = df.loc[i, f"atm_vol_{expiry_2}"]/100

        if df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and df.loc[i, f"skew_1_{expiry_1}"] > df.loc[i, f"skew_1_{expiry_2}"] and df.loc[i+1, "base_change_1"] > -0.45:

            df.at[i,"positions"] = [{"strike":base_val_1*(1+sd*atm_vol_1*((dte_1/365)**0.5)), "expiry": expiry_1, "option_type": "call", "size": -10},
                                    {"strike":base_val_1*(1-sd*atm_vol_1*((dte_1/365)**0.5)), "expiry": expiry_1, "option_type": "put", "size": 10},
                                    {"strike":base_val_2*(1+sd*atm_vol_2*((dte_2/365)**0.5)), "expiry": expiry_2, "option_type": "call", "size": 10},
                                    {"strike":base_val_2*(1-sd*atm_vol_2*((dte_2/365)**0.5)), "expiry": expiry_2, "option_type": "put", "size": -10}]

        elif df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and df.loc[i, f"skew_1_{expiry_1}"] < df.loc[i, f"skew_1_{expiry_2}"] and df.loc[i+1, "base_change_1"] > -0.45:

            df.at[i,"positions"] = [{"strike":base_val_1*(1+sd*atm_vol_1*((dte_1/365)**0.5)), "expiry": expiry_1, "option_type": "call", "size": 10},
                                    {"strike":base_val_1*(1-sd*atm_vol_1*((dte_1/365)**0.5)), "expiry": expiry_1, "option_type": "put", "size": -10},
                                    {"strike":base_val_2*(1+sd*atm_vol_2*((dte_2/365)**0.5)), "expiry": expiry_2, "option_type": "call", "size": -10},
                                    {"strike":base_val_2*(1-sd*atm_vol_2*((dte_2/365)**0.5)), "expiry": expiry_2, "option_type": "put", "size": 10}]
        else:
            df.at[i,"positions"] = [{"strike":base_val_1, "expiry": expiry_1, "option_type": "call", "size": 0}]

    return df

# Gamma Arbitrage

def iv_rv_arb_ma(df, expiry, lookback, atm_qty):

    df["realised_vol"] = 1600 * abs(df[f"base_val_{expiry}"] - df[f"base_val_{expiry}"].shift(1))/df[f"base_val_{expiry}"].shift(1)
    df.loc[df["expiry_date_1"] != df["expiry_date_1"].shift(1), "realised_vol"] = 1600 * abs(df[f"base_val_{expiry}"] - df[f"base_val_{expiry + 1}"].shift(1))/df[f"base_val_{expiry + 1}"].shift(1)
    df["rvma"] = df["realised_vol"].rolling(window=lookback).mean()
    df["rvrms"] = np.sqrt((df["realised_vol"]**2).rolling(window=lookback).mean())

    for i in range(len(df)-1):

        base_val = df.loc[i, f"base_val_{expiry}"]

        if df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and df.loc[i,  f"atm_vol_{expiry}"] > df.loc[i, "rvma"] and df.loc[i+1, "base_change_1"] > -0.45:

            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": -atm_qty * 10},
                                    {"strike":base_val, "expiry": expiry, "option_type": "put", "size": -atm_qty * 10}]
                                    
        else:
            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": 0}]

    return df

def iv_rv_arb_rms(df, expiry, lookback, atm_qty):

    df["realised_vol"] = 1600 * abs(df[f"base_val_{expiry}"] - df[f"base_val_{expiry}"].shift(1))/df[f"base_val_{expiry}"].shift(1)
    df.loc[df["expiry_date_1"] != df["expiry_date_1"].shift(1), "realised_vol"] = 1600 * abs(df[f"base_val_{expiry}"] - df[f"base_val_{expiry + 1}"].shift(1))/df[f"base_val_{expiry + 1}"].shift(1)
    df["rvma"] = df["realised_vol"].rolling(window=lookback).mean()
    df["rvrms"] = np.sqrt((df["realised_vol"]**2).rolling(window=lookback).mean())

    for i in range(len(df)-1):

        base_val = df.loc[i, f"base_val_{expiry}"]

        if df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and df.loc[i,  f"atm_vol_{expiry}"] > df.loc[i, "rvrms"] and df.loc[i+1, "base_change_1"] > -0.45:

            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": -atm_qty * 10},
                                    {"strike":base_val, "expiry": expiry, "option_type": "put", "size": -atm_qty * 10}]
                                    
        else:
            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": 0}]

    return df

# Vol reversion strategies

def vol_percentile_reversion_long(df, expiry, lookback, percentile):

    df["atm_vol_percentile"] = df[f"atm_vol_{expiry}"].rolling(window=lookback).quantile(percentile/100)
    df = df.iloc[lookback - 1:].reset_index(drop=True)

    for i in range(len(df)-1):

        base_val = df.loc[i, f"base_val_{expiry}"]

        if df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and df.loc[i, f"atm_vol_{expiry}"] <= df.loc[i, "atm_vol_percentile"] and df.loc[i+1, "base_change_1"] > -0.45:
                                                
            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": 10},
                                    {"strike":base_val, "expiry": expiry, "option_type": "put", "size": 10}]

        else:
            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": 0}]

    return df


def vol_percentile_reversion_short(df, expiry, lookback, percentile):

    df["atm_vol_percentile"] = df[f"atm_vol_{expiry}"].rolling(window=lookback).quantile(percentile/100)
    df = df.iloc[lookback - 1:].reset_index(drop=True)

    for i in range(len(df)-1):

        base_val = df.loc[i, f"base_val_{expiry}"]

        if df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and df.loc[i, f"atm_vol_{expiry}"] >= df.loc[i, "atm_vol_percentile"] and df.loc[i+1, "base_change_1"] > -0.45:
                                                
            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": -10},
                                    {"strike":base_val, "expiry": expiry, "option_type": "put", "size": -10}]

        else:
            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": 0}]

    return df

# Skew reversion strategies

def slope_percentile_reversion_long(df, expiry, factor, sd, lookback, percentile): # factor in string format / long slope denotes long the calls and short the puts

    df["slope_percentile"] = df[f"slope{factor}_{expiry}"].rolling(window=lookback).quantile(percentile/100)
    df = df.iloc[lookback - 1:].reset_index(drop=True)

    for i in range(len(df)-1):

        base_val = df.loc[i, f"base_val_{expiry}"]
        dte = df.loc[i, f"DTE_{expiry}"]
        atm_vol = df.loc[i, f"atm_vol_{expiry}"]/100

        delta_hedge_ratio = (get_greeks_ratio(base_val,atm_vol,sd)["call_delta_ratio"] + get_greeks_ratio(base_val,atm_vol,sd)["put_delta_ratio"]) / 2

        if df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and df.loc[i, f"slope{factor}_{expiry}"] <= df.loc[i, "slope_percentile"] and df.loc[i+1, "base_change_1"] > -0.45:
                                                
            df.at[i,"positions"] = [{"strike":base_val*(1+sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "call", "size": 10},
                                    {"strike":base_val*(1-sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "put", "size": -10},
                                    {"strike":base_val, "expiry": expiry, "option_type": "call", "size": -delta_hedge_ratio*10}, # this is the delta hedging component
                                    {"strike":base_val, "expiry": expiry, "option_type": "put", "size": delta_hedge_ratio*10}]

        else:
            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": 0}]

    return df

def slope_percentile_reversion_short(df, expiry, factor, sd, lookback, percentile): # factor in string format

    df["slope_percentile"] = df[f"slope{factor}_{expiry}"].rolling(window=lookback).quantile(percentile/100)
    df = df.iloc[lookback - 1:].reset_index(drop=True)

    for i in range(len(df)-1):

        base_val = df.loc[i, f"base_val_{expiry}"]
        dte = df.loc[i, f"DTE_{expiry}"]
        atm_vol = df.loc[i, f"atm_vol_{expiry}"]/100

        delta_hedge_ratio = (get_greeks_ratio(base_val,atm_vol,sd)["call_delta_ratio"] + get_greeks_ratio(base_val,atm_vol,sd)["put_delta_ratio"]) / 2

        if df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and df.loc[i, f"slope{factor}_{expiry}"] >= df.loc[i, "slope_percentile"] and df.loc[i+1, "base_change_1"] > -0.45:
                                                
            df.at[i,"positions"] = [{"strike":base_val*(1+sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "call", "size": -10},
                                    {"strike":base_val*(1-sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "put", "size": 10},
                                    {"strike":base_val, "expiry": expiry, "option_type": "call", "size": delta_hedge_ratio*10}, # this is the delta hedging component
                                    {"strike":base_val, "expiry": expiry, "option_type": "put", "size": -delta_hedge_ratio*10}]


        else:
            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": 0}]

    return df


def skew_percentile_reversion_long(df, expiry, factor, sd, lookback, percentile): # factor in string format / long slope denotes long the calls and short the puts

    df["skew_percentile"] = df[f"skew_{factor}_{expiry}"].rolling(window=lookback).quantile(percentile/100)
    df = df.iloc[lookback - 1:].reset_index(drop=True)

    for i in range(len(df)-1):

        base_val = df.loc[i, f"base_val_{expiry}"]
        dte = df.loc[i, f"DTE_{expiry}"]
        atm_vol = df.loc[i, f"atm_vol_{expiry}"]/100

        delta_hedge_ratio = (get_greeks_ratio(base_val,atm_vol,sd)["call_delta_ratio"] + get_greeks_ratio(base_val,atm_vol,sd)["put_delta_ratio"]) / 2

        if df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and df.loc[i, f"skew_{factor}_{expiry}"] <= df.loc[i, "skew_percentile"] and df.loc[i+1, "base_change_1"] > -0.45:
                                                
            df.at[i,"positions"] = [{"strike":base_val*(1+sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "call", "size": 10},
                                    {"strike":base_val*(1-sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "put", "size": -10},
                                    {"strike":base_val, "expiry": expiry, "option_type": "call", "size": -delta_hedge_ratio*10}, # this is the delta hedging component
                                    {"strike":base_val, "expiry": expiry, "option_type": "put", "size": delta_hedge_ratio*10}]

        else:
            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": 0}]

    return df

def skew_percentile_reversion_short(df, expiry, factor, sd, lookback, percentile): # factor in string format / long slope denotes long the calls and short the puts

    df["skew_percentile"] = df[f"skew_{factor}_{expiry}"].rolling(window=lookback).quantile(percentile/100)
    df = df.iloc[lookback - 1:].reset_index(drop=True)

    for i in range(len(df)-1):

        base_val = df.loc[i, f"base_val_{expiry}"]
        dte = df.loc[i, f"DTE_{expiry}"]
        atm_vol = df.loc[i, f"atm_vol_{expiry}"]/100

        delta_hedge_ratio = (get_greeks_ratio(base_val,atm_vol,sd)["call_delta_ratio"] + get_greeks_ratio(base_val,atm_vol,sd)["put_delta_ratio"]) / 2

        if df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and df.loc[i, f"skew_{factor}_{expiry}"] >= df.loc[i, "skew_percentile"] and df.loc[i+1, "base_change_1"] > -0.45:
                                                
            df.at[i,"positions"] = [{"strike":base_val*(1+sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "call", "size": -10},
                                    {"strike":base_val*(1-sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "put", "size": 10},
                                    {"strike":base_val, "expiry": expiry, "option_type": "call", "size": delta_hedge_ratio*10}, # this is the delta hedging component
                                    {"strike":base_val, "expiry": expiry, "option_type": "put", "size": -delta_hedge_ratio*10}]

        else:
            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": 0}]

    return df

# Kurtosis reversion strategies

def kurt_percentile_reversion_long(df, expiry, factor, sd, threshold): # factor in string format / long slope denotes long the calls and short the puts

    for i in range(len(df)-1):

        base_val = df.loc[i, f"base_val_{expiry}"]
        dte = df.loc[i, f"DTE_{expiry}"]
        atm_vol = df.loc[i, f"atm_vol_{expiry}"]/100

        gamma_hedge_ratio = (get_greeks_ratio(base_val,atm_vol,sd)["call_gamma_ratio"] + get_greeks_ratio(base_val,atm_vol,sd)["put_gamma_ratio"]) / 2

        if df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and df.loc[i, f"kurt_{factor}_{expiry}"] <= threshold and df.loc[i+1, "base_change_1"] > -0.45:
                                                
            df.at[i,"positions"] = [{"strike":base_val*(1+sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "call", "size": 10},
                                    {"strike":base_val*(1-sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "put", "size": 10},
                                    {"strike":base_val, "expiry": expiry, "option_type": "call", "size": -gamma_hedge_ratio*10},  # trade the ATMs to become more vega and gamma neutral
                                    {"strike":base_val, "expiry": expiry, "option_type": "put", "size": -gamma_hedge_ratio*10}]

        else:
            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": 0}]

    return df

def kurt_percentile_reversion_short(df, expiry, factor, sd, threshold): # factor in string format / long slope denotes long the calls and short the puts

    for i in range(len(df)-1):

        base_val = df.loc[i, f"base_val_{expiry}"]
        dte = df.loc[i, f"DTE_{expiry}"]
        atm_vol = df.loc[i, f"atm_vol_{expiry}"]/100

        gamma_hedge_ratio = (get_greeks_ratio(base_val,atm_vol,sd)["call_gamma_ratio"] + get_greeks_ratio(base_val,atm_vol,sd)["put_gamma_ratio"]) / 2

        if df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and df.loc[i, f"kurt_{factor}_{expiry}"] >= threshold and df.loc[i+1, "base_change_1"] > -0.45:
                                                
            df.at[i,"positions"] = [{"strike":base_val*(1+sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "call", "size": -10},
                                    {"strike":base_val*(1-sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "put", "size": -10},
                                    {"strike":base_val, "expiry": expiry, "option_type": "call", "size": gamma_hedge_ratio*10},  # trade the ATMs to become more vega and gamma neutral
                                    {"strike":base_val, "expiry": expiry, "option_type": "put", "size": gamma_hedge_ratio*10}]

        else:
            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": 0}]

    return df

# Single options strategies (delta/gamma unhedged)

def single_option_upside_long_dugu(df, expiry, factor, sd, lookback, skew_percentile, kurt_percentile): # factor in string format / long slope denotes long the calls and short the puts

    df["skew_percentile"] = df[f"skew_{factor}_{expiry}"].rolling(window=lookback).quantile(skew_percentile/100)
    df["kurt_percentile"] = df[f"kurt_{factor}_{expiry}"].rolling(window=lookback).quantile(kurt_percentile/100)
    df = df.iloc[lookback - 1:].reset_index(drop=True)

    for i in range(len(df)-1):

        base_val = df.loc[i, f"base_val_{expiry}"]
        dte = df.loc[i, f"DTE_{expiry}"]
        atm_vol = df.loc[i, f"atm_vol_{expiry}"]/100

        delta_hedge_ratio = get_greeks_ratio(base_val,atm_vol,sd)["call_delta_ratio"]
        gamma_hedge_ratio = get_greeks_ratio(base_val,atm_vol,sd)["call_gamma_ratio"]

        if df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and df.loc[i, f"skew_{factor}_{expiry}"] <= df.loc[i, "skew_percentile"] and df.loc[i, f"kurt_{factor}_{expiry}"] <= df.loc[i, "kurt_percentile"] and df.loc[i+1, "base_change_1"] > -0.45:
                                                
            df.at[i,"positions"] = [{"strike":base_val*(1+sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "call", "size": 10}]

        else:
            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": 0}]

    return df

def single_option_upside_short_dugu(df, expiry, factor, sd, lookback, skew_percentile, kurt_percentile): # factor in string format / long slope denotes long the calls and short the puts

    df["skew_percentile"] = df[f"skew_{factor}_{expiry}"].rolling(window=lookback).quantile(skew_percentile/100)
    df["kurt_percentile"] = df[f"kurt_{factor}_{expiry}"].rolling(window=lookback).quantile(kurt_percentile/100)
    df = df.iloc[lookback - 1:].reset_index(drop=True)

    for i in range(len(df)-1):

        base_val = df.loc[i, f"base_val_{expiry}"]
        dte = df.loc[i, f"DTE_{expiry}"]
        atm_vol = df.loc[i, f"atm_vol_{expiry}"]/100

        delta_hedge_ratio = get_greeks_ratio(base_val,atm_vol,sd)["call_delta_ratio"]
        gamma_hedge_ratio = get_greeks_ratio(base_val,atm_vol,sd)["call_gamma_ratio"]

        if df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and df.loc[i, f"skew_{factor}_{expiry}"] >= df.loc[i, "skew_percentile"] and df.loc[i, f"kurt_{factor}_{expiry}"] >= df.loc[i, "kurt_percentile"] and df.loc[i+1, "base_change_1"] > -0.45:
                                                
            df.at[i,"positions"] = [{"strike":base_val*(1+sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "call", "size": -10}]

        else:
            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": 0}]

    return df

def single_option_downside_long_dugu(df, expiry, factor, sd, lookback, skew_percentile, kurt_percentile): # factor in string format / long slope denotes long the calls and short the puts

    df["skew_percentile"] = df[f"skew_{factor}_{expiry}"].rolling(window=lookback).quantile(skew_percentile/100)
    df["kurt_percentile"] = df[f"kurt_{factor}_{expiry}"].rolling(window=lookback).quantile(kurt_percentile/100)
    df = df.iloc[lookback - 1:].reset_index(drop=True)

    for i in range(len(df)-1):

        base_val = df.loc[i, f"base_val_{expiry}"]
        dte = df.loc[i, f"DTE_{expiry}"]
        atm_vol = df.loc[i, f"atm_vol_{expiry}"]/100

        delta_hedge_ratio = get_greeks_ratio(base_val,atm_vol,sd)["put_delta_ratio"]
        gamma_hedge_ratio = get_greeks_ratio(base_val,atm_vol,sd)["put_gamma_ratio"]

        if df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and df.loc[i, f"skew_{factor}_{expiry}"] >= df.loc[i, "skew_percentile"] and df.loc[i, f"kurt_{factor}_{expiry}"] <= df.loc[i, "kurt_percentile"] and df.loc[i+1, "base_change_1"] > -0.45:
                                                
            df.at[i,"positions"] = [{"strike":base_val*(1+sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "put", "size": 10}]

        else:
            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": 0}]

    return df

def single_option_downside_short_dugu(df, expiry, factor, sd, lookback, skew_percentile, kurt_percentile): # factor in string format / long slope denotes long the calls and short the puts

    df["skew_percentile"] = df[f"skew_{factor}_{expiry}"].rolling(window=lookback).quantile(skew_percentile/100)
    df["kurt_percentile"] = df[f"kurt_{factor}_{expiry}"].rolling(window=lookback).quantile(kurt_percentile/100)
    df = df.iloc[lookback - 1:].reset_index(drop=True)

    for i in range(len(df)-1):

        base_val = df.loc[i, f"base_val_{expiry}"]
        dte = df.loc[i, f"DTE_{expiry}"]
        atm_vol = df.loc[i, f"atm_vol_{expiry}"]/100

        delta_hedge_ratio = get_greeks_ratio(base_val,atm_vol,sd)["put_delta_ratio"]
        gamma_hedge_ratio = get_greeks_ratio(base_val,atm_vol,sd)["put_gamma_ratio"]

        if df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and df.loc[i, f"skew_{factor}_{expiry}"] <= df.loc[i, "skew_percentile"] and df.loc[i, f"kurt_{factor}_{expiry}"] >= df.loc[i, "kurt_percentile"] and df.loc[i+1, "base_change_1"] > -0.45:
                                                
            df.at[i,"positions"] = [{"strike":base_val*(1+sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "put", "size": -10}]
            
        else:
            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": 0}]

    return df

# Single options strategies (gamma unhedged)

def single_option_upside_long_gu(df, expiry, factor, sd, lookback, skew_percentile, kurt_percentile): # factor in string format / long slope denotes long the calls and short the puts

    df["skew_percentile"] = df[f"skew_{factor}_{expiry}"].rolling(window=lookback).quantile(skew_percentile/100)
    df["kurt_percentile"] = df[f"kurt_{factor}_{expiry}"].rolling(window=lookback).quantile(kurt_percentile/100)
    df = df.iloc[lookback - 1:].reset_index(drop=True)

    for i in range(len(df)-1):

        base_val = df.loc[i, f"base_val_{expiry}"]
        dte = df.loc[i, f"DTE_{expiry}"]
        atm_vol = df.loc[i, f"atm_vol_{expiry}"]/100

        delta_hedge_ratio = get_greeks_ratio(base_val,atm_vol,sd)["call_delta_ratio"]
        gamma_hedge_ratio = get_greeks_ratio(base_val,atm_vol,sd)["call_gamma_ratio"]

        if df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and df.loc[i, f"skew_{factor}_{expiry}"] <= df.loc[i, "skew_percentile"] and df.loc[i, f"kurt_{factor}_{expiry}"] <= df.loc[i, "kurt_percentile"] and df.loc[i+1, "base_change_1"] > -0.45:
                                                
            df.at[i,"positions"] = [{"strike":base_val*(1+sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "call", "size": 10},

                                    {"strike":base_val, "expiry": expiry, "option_type": "call", "size": -delta_hedge_ratio*10}, # this is the delta hedging component
                                    {"strike":base_val, "expiry": expiry, "option_type": "put", "size": delta_hedge_ratio*10}]

        else:
            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": 0}]

    return df

def single_option_upside_short_gu(df, expiry, factor, sd, lookback, skew_percentile, kurt_percentile): # factor in string format / long slope denotes long the calls and short the puts

    df["skew_percentile"] = df[f"skew_{factor}_{expiry}"].rolling(window=lookback).quantile(skew_percentile/100)
    df["kurt_percentile"] = df[f"kurt_{factor}_{expiry}"].rolling(window=lookback).quantile(kurt_percentile/100)
    df = df.iloc[lookback - 1:].reset_index(drop=True)

    for i in range(len(df)-1):

        base_val = df.loc[i, f"base_val_{expiry}"]
        dte = df.loc[i, f"DTE_{expiry}"]
        atm_vol = df.loc[i, f"atm_vol_{expiry}"]/100

        delta_hedge_ratio = get_greeks_ratio(base_val,atm_vol,sd)["call_delta_ratio"]
        gamma_hedge_ratio = get_greeks_ratio(base_val,atm_vol,sd)["call_gamma_ratio"]

        if df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and df.loc[i, f"skew_{factor}_{expiry}"] >= df.loc[i, "skew_percentile"] and df.loc[i, f"kurt_{factor}_{expiry}"] >= df.loc[i, "kurt_percentile"] and df.loc[i+1, "base_change_1"] > -0.45:
                                                
            df.at[i,"positions"] = [{"strike":base_val*(1+sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "call", "size": -10},

                                    {"strike":base_val, "expiry": expiry, "option_type": "call", "size": delta_hedge_ratio*10}, # this is the delta hedging component
                                    {"strike":base_val, "expiry": expiry, "option_type": "put", "size": -delta_hedge_ratio*10}]

        else:
            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": 0}]

    return df

def single_option_downside_long_gu(df, expiry, factor, sd, lookback, skew_percentile, kurt_percentile): # factor in string format / long slope denotes long the calls and short the puts

    df["skew_percentile"] = df[f"skew_{factor}_{expiry}"].rolling(window=lookback).quantile(skew_percentile/100)
    df["kurt_percentile"] = df[f"kurt_{factor}_{expiry}"].rolling(window=lookback).quantile(kurt_percentile/100)
    df = df.iloc[lookback - 1:].reset_index(drop=True)

    for i in range(len(df)-1):

        base_val = df.loc[i, f"base_val_{expiry}"]
        dte = df.loc[i, f"DTE_{expiry}"]
        atm_vol = df.loc[i, f"atm_vol_{expiry}"]/100

        delta_hedge_ratio = get_greeks_ratio(base_val,atm_vol,sd)["put_delta_ratio"]
        gamma_hedge_ratio = get_greeks_ratio(base_val,atm_vol,sd)["put_gamma_ratio"]

        if df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and df.loc[i, f"skew_{factor}_{expiry}"] >= df.loc[i, "skew_percentile"] and df.loc[i, f"kurt_{factor}_{expiry}"] <= df.loc[i, "kurt_percentile"] and df.loc[i+1, "base_change_1"] > -0.45:
                                                
            df.at[i,"positions"] = [{"strike":base_val*(1+sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "put", "size": 10},
                                    {"strike":base_val, "expiry": expiry, "option_type": "call", "size": delta_hedge_ratio*10}, # this is the delta hedging component
                                    {"strike":base_val, "expiry": expiry, "option_type": "put", "size": -delta_hedge_ratio*10}]

        else:
            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": 0}]

    return df

def single_option_downside_short_gu(df, expiry, factor, sd, lookback, skew_percentile, kurt_percentile): # factor in string format / long slope denotes long the calls and short the puts

    df["skew_percentile"] = df[f"skew_{factor}_{expiry}"].rolling(window=lookback).quantile(skew_percentile/100)
    df["kurt_percentile"] = df[f"kurt_{factor}_{expiry}"].rolling(window=lookback).quantile(kurt_percentile/100)
    df = df.iloc[lookback - 1:].reset_index(drop=True)

    for i in range(len(df)-1):

        base_val = df.loc[i, f"base_val_{expiry}"]
        dte = df.loc[i, f"DTE_{expiry}"]
        atm_vol = df.loc[i, f"atm_vol_{expiry}"]/100

        delta_hedge_ratio = get_greeks_ratio(base_val,atm_vol,sd)["put_delta_ratio"]
        gamma_hedge_ratio = get_greeks_ratio(base_val,atm_vol,sd)["put_gamma_ratio"]

        if df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and df.loc[i, f"skew_{factor}_{expiry}"] <= df.loc[i, "skew_percentile"] and df.loc[i, f"kurt_{factor}_{expiry}"] >= df.loc[i, "kurt_percentile"] and df.loc[i+1, "base_change_1"] > -0.45:
                                                
            df.at[i,"positions"] = [{"strike":base_val*(1+sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "put", "size": -10},

                                    {"strike":base_val, "expiry": expiry, "option_type": "call", "size": -delta_hedge_ratio*10}, # this is the delta hedging component
                                    {"strike":base_val, "expiry": expiry, "option_type": "put", "size": delta_hedge_ratio*10}]

        else:
            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": 0}]

    return df

# Single options strategies (delta/gamma hedged)

def single_option_upside_long(df, expiry, factor, sd, lookback, skew_percentile, kurt_percentile): # factor in string format / long slope denotes long the calls and short the puts

    df["skew_percentile"] = df[f"skew_{factor}_{expiry}"].rolling(window=lookback).quantile(skew_percentile/100)
    df["kurt_percentile"] = df[f"kurt_{factor}_{expiry}"].rolling(window=lookback).quantile(kurt_percentile/100)
    df = df.iloc[lookback - 1:].reset_index(drop=True)

    for i in range(len(df)-1):

        base_val = df.loc[i, f"base_val_{expiry}"]
        dte = df.loc[i, f"DTE_{expiry}"]
        atm_vol = df.loc[i, f"atm_vol_{expiry}"]/100

        delta_hedge_ratio = get_greeks_ratio(base_val,atm_vol,sd)["call_delta_ratio"]
        gamma_hedge_ratio = get_greeks_ratio(base_val,atm_vol,sd)["call_gamma_ratio"]

        if df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and df.loc[i, f"skew_{factor}_{expiry}"] <= df.loc[i, "skew_percentile"] and df.loc[i, f"kurt_{factor}_{expiry}"] <= df.loc[i, "kurt_percentile"] and df.loc[i+1, "base_change_1"] > -0.45:
                                                
            df.at[i,"positions"] = [{"strike":base_val*(1+sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "call", "size": 10},

                                    {"strike":base_val, "expiry": expiry, "option_type": "call", "size": -delta_hedge_ratio*10-gamma_hedge_ratio*5}, # this is the delta hedging component
                                    {"strike":base_val, "expiry": expiry, "option_type": "put", "size": delta_hedge_ratio*10-gamma_hedge_ratio*5}]

        else:
            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": 0}]

    return df

def single_option_upside_short(df, expiry, factor, sd, lookback, skew_percentile, kurt_percentile): # factor in string format / long slope denotes long the calls and short the puts

    df["skew_percentile"] = df[f"skew_{factor}_{expiry}"].rolling(window=lookback).quantile(skew_percentile/100)
    df["kurt_percentile"] = df[f"kurt_{factor}_{expiry}"].rolling(window=lookback).quantile(kurt_percentile/100)
    df = df.iloc[lookback - 1:].reset_index(drop=True)

    for i in range(len(df)-1):

        base_val = df.loc[i, f"base_val_{expiry}"]
        dte = df.loc[i, f"DTE_{expiry}"]
        atm_vol = df.loc[i, f"atm_vol_{expiry}"]/100

        delta_hedge_ratio = get_greeks_ratio(base_val,atm_vol,sd)["call_delta_ratio"]
        gamma_hedge_ratio = get_greeks_ratio(base_val,atm_vol,sd)["call_gamma_ratio"]

        if df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and df.loc[i, f"skew_{factor}_{expiry}"] >= df.loc[i, "skew_percentile"] and df.loc[i, f"kurt_{factor}_{expiry}"] >= df.loc[i, "kurt_percentile"] and df.loc[i+1, "base_change_1"] > -0.45:
                                                
            df.at[i,"positions"] = [{"strike":base_val*(1+sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "call", "size": -10},

                                    {"strike":base_val, "expiry": expiry, "option_type": "call", "size": delta_hedge_ratio*10+gamma_hedge_ratio*5}, # this is the delta hedging component
                                    {"strike":base_val, "expiry": expiry, "option_type": "put", "size": -delta_hedge_ratio*10+gamma_hedge_ratio*5}]

        else:
            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": 0}]

    return df

def single_option_downside_long(df, expiry, factor, sd, lookback, skew_percentile, kurt_percentile): # factor in string format / long slope denotes long the calls and short the puts

    df["skew_percentile"] = df[f"skew_{factor}_{expiry}"].rolling(window=lookback).quantile(skew_percentile/100)
    df["kurt_percentile"] = df[f"kurt_{factor}_{expiry}"].rolling(window=lookback).quantile(kurt_percentile/100)
    df = df.iloc[lookback - 1:].reset_index(drop=True)

    for i in range(len(df)-1):

        base_val = df.loc[i, f"base_val_{expiry}"]
        dte = df.loc[i, f"DTE_{expiry}"]
        atm_vol = df.loc[i, f"atm_vol_{expiry}"]/100

        delta_hedge_ratio = get_greeks_ratio(base_val,atm_vol,sd)["put_delta_ratio"]
        gamma_hedge_ratio = get_greeks_ratio(base_val,atm_vol,sd)["put_gamma_ratio"]

        if df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and df.loc[i, f"skew_{factor}_{expiry}"] >= df.loc[i, "skew_percentile"] and df.loc[i, f"kurt_{factor}_{expiry}"] <= df.loc[i, "kurt_percentile"] and df.loc[i+1, "base_change_1"] > -0.45:
                                                
            df.at[i,"positions"] = [{"strike":base_val*(1+sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "put", "size": 10},
                                    {"strike":base_val, "expiry": expiry, "option_type": "call", "size": delta_hedge_ratio*10-gamma_hedge_ratio*5}, # this is the delta hedging component
                                    {"strike":base_val, "expiry": expiry, "option_type": "put", "size": -delta_hedge_ratio*10-gamma_hedge_ratio*5}]

        else:
            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": 0}]

    return df

def single_option_downside_short(df, expiry, factor, sd, lookback, skew_percentile, kurt_percentile): # factor in string format / long slope denotes long the calls and short the puts

    df["skew_percentile"] = df[f"skew_{factor}_{expiry}"].rolling(window=lookback).quantile(skew_percentile/100)
    df["kurt_percentile"] = df[f"kurt_{factor}_{expiry}"].rolling(window=lookback).quantile(kurt_percentile/100)
    df = df.iloc[lookback - 1:].reset_index(drop=True)

    for i in range(len(df)-1):

        base_val = df.loc[i, f"base_val_{expiry}"]
        dte = df.loc[i, f"DTE_{expiry}"]
        atm_vol = df.loc[i, f"atm_vol_{expiry}"]/100

        delta_hedge_ratio = get_greeks_ratio(base_val,atm_vol,sd)["put_delta_ratio"]
        gamma_hedge_ratio = get_greeks_ratio(base_val,atm_vol,sd)["put_gamma_ratio"]

        if df.loc[i, "expiry_date_1"] == df.loc[i+1, "expiry_date_1"] and df.loc[i, f"skew_{factor}_{expiry}"] <= df.loc[i, "skew_percentile"] and df.loc[i, f"kurt_{factor}_{expiry}"] >= df.loc[i, "kurt_percentile"] and df.loc[i+1, "base_change_1"] > -0.45:
                                                
            df.at[i,"positions"] = [{"strike":base_val*(1+sd*atm_vol*((dte/365)**0.5)), "expiry": expiry, "option_type": "put", "size": -10},

                                    {"strike":base_val, "expiry": expiry, "option_type": "call", "size": -delta_hedge_ratio*10+gamma_hedge_ratio*5}, # this is the delta hedging component
                                    {"strike":base_val, "expiry": expiry, "option_type": "put", "size": delta_hedge_ratio*10+gamma_hedge_ratio*5}]

        else:
            df.at[i,"positions"] = [{"strike":base_val, "expiry": expiry, "option_type": "call", "size": 0}]

    return df