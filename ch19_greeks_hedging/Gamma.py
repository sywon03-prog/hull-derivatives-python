import numpy as np
from scipy.stats import norm
from bs import d1_d2

#d2f / dS2
def Gamma(S, K, r, sigma, T, q):
    d1, d2 = d1_d2(S, K, r, sigma, T, q)
    gamma = (norm.pdf(d1) * np.exp(-q * T)) / (S * sigma * np.sqrt(T))
    return gamma


if __name__ == "__main__":
    # Hull 19장 예제
    S, K, r, q, sigma, T = 49, 50, 0.05, 0.0, 0.20, 20 / 52
    print(f"gamma  = {Gamma(S, K, r, sigma, T, q):.3f}   (책: 0.066)")