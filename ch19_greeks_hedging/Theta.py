import numpy as np
from scipy.stats import norm
from bs import d1_d2

#df / dt
def Theta(S, K, r, sigma, T, q,option_type) :
    d1,d2 = d1_d2(S, K, r, sigma, T, q)

    if(option_type == "call") : 
        Theta = (-S * norm.pdf(d1) * sigma * np.exp(- q * T)) / (2 * np.sqrt(T)) + (q * S * norm.cdf(d1) * np.exp(-q * T )) - (r * K * np.exp(-r * T) * norm.cdf(d2))

    else :
        Theta = (-S * norm.pdf(d1) * sigma * np.exp(- q * T)) / (2 * np.sqrt(T)) - (q * S * norm.cdf(-d1) * np.exp(-q * T )) + (r * K * np.exp(-r * T) * norm.cdf(-d2))

    return Theta



if __name__ == "__main__":
    # Hull 19장 예제
    S, K, r, q, sigma, T = 49, 50, 0.05, 0.0, 0.20, 20 / 52
    print(f"theta  = {Theta(S, K, r, sigma, T, q,option_type = "call"):.2f} / 년, "
          f"{Theta(S, K, r, sigma, T, q,option_type = "call") / 365:.4f} / 일   (책: -4.31, -0.0118)")