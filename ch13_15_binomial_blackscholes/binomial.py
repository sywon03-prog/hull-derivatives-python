import numpy as np
import math 

def binomial(S, K, r, sigma, T, n,option_type = "call"):
    dt = T / n
    u = np.exp(sigma * np.sqrt(dt))
    d = np.exp(-sigma * np.sqrt(dt))
    p = (np.exp(r*dt) - d) / (u - d)
    expected_value  = 0
    j = 0
    if option_type == "call":
        for j in range(n + 1) :
            case = math.comb(n, j) * (p**(j)) * ((1-p)**(n-j)) * max(S * (u**(j)) * (d**(n-j)) - K, 0 )
            expected_value += case

        f = np.exp(-r*T) * expected_value 
        return f
    else :
        for j in range(n + 1) :
            case = math.comb(n, j) * (p**(j)) * ((1-p)**(n-j)) * max(K - S * (u**(j))* (d**(n-j)), 0 )
            expected_value += case

        f = np.exp(-r*T) * expected_value 
        return f


def binomial_backward(S, K, r, sigma, T, n,option_type = "call"):
    dt = T / n
    u = np.exp(sigma * np.sqrt(dt))
    d = np.exp(-sigma * np.sqrt(dt))
    p = (np.exp(r*dt) - d) / (u - d)
    disc = np.exp(-r * dt)
    j = np.arange(n,-1,-1)
    ST = S * (u**(j)) * (d**(n-j))
    if option_type == "call":
        value = np.maximum(ST - K , 0)
    else :
        value = np.maximum(K - ST , 0)

    if option_type == "american_put" :
        for i in range(n, 0 , -1) :
            for k in range(0, i) :
                f_mid = disc * (value[k] * p + value[k+1] * (1-p))
                S_mid = S * (u**(i - k - 1) * (d**(k)))
                value[k] = max(f_mid, K - S_mid)
        return value[0]
    # 유러피안 콜,풋은 조기행사 불가, 아메리칸 콜은 무배당의 경우 조기행사가 불리하므로 아래방식으로 계산.
    else :
        for i in range(n, 0 , -1) :
            for k in range(0, i) :
                f_mid = disc * (value[k] * p + value[k+1] * (1-p))
                value[k] = f_mid         
        return value[0]


def put_call_parity(S,K,r,T) :
    p = binomial_backward(S=42, K=40, r=0.10, sigma=0.20, T=0.5, n = 1000,option_type="put")
    c = binomial_backward(S=42, K=40, r=0.10, sigma=0.20, T=0.5, n = 1000,option_type="call")
    return np.isclose(c - p, S - K * np.exp(-r * T))

if __name__ == "__main__":
    # Hull 15장 예제 입력 (S=42, K=40, r=10%, sigma=20%, T=0.5)
    price = binomial(S=42, K=40, r=0.10, sigma=0.20, T=0.5, n = 1000,option_type="call")
    print(f"다기간 이항모형 콜 가격: {price:.4f}")
    price = binomial_backward(S=42, K=40, r=0.10, sigma=0.20, T=0.5, n = 1000,option_type="call")
    print(f"다기간 이항모형 콜 가격(역순 계산): {price:.4f}")
    print(f"풋 - 콜 패리티 검증 : {put_call_parity(S=42, K=40, r=0.10, T = 0.5)}")