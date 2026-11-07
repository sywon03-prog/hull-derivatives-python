import numpy as np
from scipy.stats import norm



def black_scholes(S, K, r, sigma, T,option_type = "call") :
    d2 = -(np.log(K) - (np.log(S) + (r - (sigma**2 / 2))*T)) / (sigma * np.sqrt(T))
    d1 = d2 + sigma*np.sqrt(T)

    if(option_type == "call"):
        c = S * norm.cdf(d1) - K*np.exp(-r * T) * norm.cdf(d2)
        return c
    else :
        p = K*np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        return p


def put_call_parity(S,K,r,T) :
    p = black_scholes(S=42, K=40, r=0.10, sigma=0.20, T=0.5,option_type = "put")
    c = black_scholes(S=42, K=40, r=0.10, sigma=0.20, T=0.5,option_type = "call")

    return np.isclose(c - p, S - K * np.exp(-r * T))

if __name__ == "__main__":
    # Hull 15장 예제 입력 (S=42, K=40, r=10%, sigma=20%, T=0.5)
    price = black_scholes(S=42, K=40, r=0.10, sigma=0.20, T=0.5,option_type = "call")
    print(f"1기간 이항모형 콜 가격: {price:.4f}")
    print(f"풋-콜 패리티 검증 : {put_call_parity(S = 42,K = 40, r = 0.10, T = 0.5)}")