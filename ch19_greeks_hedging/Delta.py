import numpy as np
from scipy.stats import norm
from bs import d1_d2

#df / dS
def Delta(S, K, r, sigma, T, q, option_type) :
    d1, d2 = d1_d2(S, K, r, sigma, T, q)
    if (option_type == "call") :
        Delta = norm.cdf(d1) * np.exp(- q * T) 
    else : 
        Delta = (norm.cdf(d1) - 1 ) * np.exp(- q * T) 

    return Delta


if __name__ == "__main__":
    # Hull 19장 예제
    S, K, r, q, sigma, T = 49, 50, 0.05, 0.0, 0.20, 20 / 52
    print(f"delta  = {Delta(S, K, r, sigma, T, q, option_type="call"):.3f}   (책: 0.522)")
