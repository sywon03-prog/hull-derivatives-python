import numpy as np
from scipy.stats import norm
from bs import d1_d2

#df/dr
def Rho(S, K, r, sigma, T, q,option_type):
    d1, d2 = d1_d2(S, K, r, sigma, T, q)
    if (option_type == "call"):
        Rho = K * T * np.exp(- r * T) * norm.cdf(d2)
    else :
        Rho = - K * T * np.exp(- r * T) * norm.cdf(-d2)

    return Rho


if __name__ == "__main__":
    # Hull 19장 예제
    S, K, r, q, sigma, T = 49, 50, 0.05, 0.0, 0.20, 20 / 52
    print(f"rho    = {Rho(S, K, r, sigma, T, q,option_type = "call"):.2f}, "
          f"{Rho(S, K, r, sigma, T, q,option_type = "call") / 100:.4f} / 1%p   (책: 8.91, 0.0891)")