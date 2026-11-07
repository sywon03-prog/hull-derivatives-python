import numpy as np


#유도 과정은 Readme
def binomial_one(S, K, r, sigma, T):
    u = np.exp(sigma * np.sqrt(T))
    d = np.exp(-sigma * np.sqrt(T))
    f_u = max(S*u - K, 0)
    f_d = max(S*d - K, 0)
    p = (np.exp(r*T) - d) / (u - d)
    f = np.exp(-r*T) * (p*f_u + (1-p)*f_d)
    return f


if __name__ == "__main__":
    # Hull 15장 예제 입력 (S=42, K=40, r=10%, sigma=20%, T=0.5)
    price = binomial_one(S=42, K=40, r=0.10, sigma=0.20, T=0.5)
    print(f"1기간 이항모형 콜 가격: {price:.4f}")
