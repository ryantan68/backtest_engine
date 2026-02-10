import numpy as np
import pandas as pd
from scipy.stats import norm

def black_scholes_greeks(
    S, K, T, r, sigma, option_type="call"
):
    """
    Returns Black-Scholes Greeks as named values:
    delta, gamma, vega, theta

    Theta: per year
    Vega: per 1.00 volatility change
    """

    if T <= 0 or sigma <= 0 or S <= 0 or K <= 0:
        return {
            "delta": np.nan,
            "gamma": np.nan,
            "vega": np.nan,
            "theta": np.nan
        }

    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    pdf_d1 = norm.pdf(d1)
    cdf_d1 = norm.cdf(d1)
    cdf_d2 = norm.cdf(d2)

    if option_type.lower() == "call":
        delta = cdf_d1
        theta = (
            - (S * pdf_d1 * sigma) / (2 * np.sqrt(T))
            - r * K * np.exp(-r * T) * cdf_d2
        )
    elif option_type.lower() == "put":
        delta = cdf_d1 - 1
        theta = (
            - (S * pdf_d1 * sigma) / (2 * np.sqrt(T))
            + r * K * np.exp(-r * T) * norm.cdf(-d2)
        )
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    gamma = pdf_d1 / (S * sigma * np.sqrt(T))
    vega = S * pdf_d1 * np.sqrt(T)

    return {
        "delta": float(delta),
        "gamma": float(gamma),
        "vega": float(vega),
        "theta": float(theta)
    }

def get_greeks_ratio(base, vol, sd):

    atm_call = black_scholes_greeks(base, base, 1, 0, vol, option_type="call")
    atm_put = black_scholes_greeks(base, base, 1, 0, vol, option_type="put")
    otm_call = black_scholes_greeks(base, base * (1+sd*vol), 1, 0, vol, option_type="call")
    otm_put = black_scholes_greeks(base, base * (1-sd*vol), 1, 0, vol, option_type="put")

    call_delta_ratio = otm_call["delta"]/atm_call["delta"]
    call_gamma_ratio = otm_call["gamma"]/atm_call["gamma"]

    put_delta_ratio = otm_put["delta"]/atm_put["delta"]
    put_gamma_ratio = otm_put["gamma"]/atm_put["gamma"]

    return {"call_delta_ratio":call_delta_ratio, 
            "call_gamma_ratio":call_gamma_ratio, 
            "put_delta_ratio":put_delta_ratio, 
            "put_gamma_ratio":put_gamma_ratio}