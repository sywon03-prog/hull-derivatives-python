import numpy as np
from scipy.stats import norm
from bs import d1_d2

#df/dsigma
def Vega(S, K, r, sigma, T, q) :
    d1,d2 = d1_d2(S, K, r, sigma, T, q)
    Vega = S * np.sqrt(T) * norm.pdf(d1) * np.exp(-q * T)
    return Vega



if __name__ == "__main__":
    # Hull 19장 예제
    S, K, r, q, sigma, T = 49, 50, 0.05, 0.0, 0.20, 20 / 52
    print(f"vega   = {Vega(S, K, r, sigma, T, q):.1f}, "
          f"{Vega(S, K, r, sigma, T, q) / 100:.3f} / 1%p   (책: 12.1, 0.121)")