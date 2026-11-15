import numpy as np
from scipy.stats import norm

def d1_d2(S, K, r, sigma, T, q) :
    d1 = -(np.log(K) - (np.log(S) + (r - q + (sigma**2 / 2))*T)) / (np.sqrt(T) * sigma)

    d2 = d1 - sigma*np.sqrt(T)
    return d1, d2

def black_scholes(S, K, r, sigma, T, q, option_type = "call") :
    d1,d2 = d1_d2(S, K, r, sigma, T, q)
    if(option_type == "call"):
        c = S*np.exp(-q * T) * norm.cdf(d1) - K*np.exp(-r * T) * norm.cdf(d2)
        return c
    else :
        p = K*np.exp(-r * T) * norm.cdf(-d2) - S* np.exp(-q * T)* norm.cdf(-d1)
        return p