import numpy as np
import matplotlib.pyplot as plt
import scienceplots
import os
BASE = os.path.dirname(os.path.abspath(__file__))
params = dict(S = 50, r = 0.05, q = 0.01, sigma = 0.3, K = 50, dt = 0.01, N = 50)

def monte_carlo(S, r, q, sigma, K, dt, N, M = 100) :
    #난수 
    eps = np.random.standard_normal((M, N))            
    next_steps = np.exp((r - q - sigma**2 / 2) * dt + sigma * np.sqrt(dt) * eps)

    result = np.ones((M, N + 1))
    result[:,0] = S
    for i in range(0,N) :
        result[:,i+1] = result[:,i] * next_steps[:,i]
    return result

result = monte_carlo(**params)
T = params["N"] * params["dt"]
N = params["N"]
t = np.linspace(0, T, N + 1)

plt.style.use(['science', 'no-latex'])

plt.figure(figsize = (8, 5))
for i in range(0,result.shape[0]) :
    plt.plot(t, result[i,:], lw = 0.8, alpha = 0.6)
plt.xlabel("Time $t$")
plt.ylabel("Stock price $S$")

#유러피언 콜 가격 계산 
print(f"{'M':>8} {'call price':>12} {'std error':>12}")
for M in [100, 1000, 10000, 100000] :
    result = monte_carlo(**params, M = M)
    exp_price = result[:,-1]
    payoff = np.maximum(exp_price - params["K"], 0)
    average = np.mean(payoff)
    current_value = average * np.exp(- params["r"] * T)
    std_error = np.std(payoff) / np.sqrt(M) * np.exp(- params["r"] * T)
    print(f"{M:>8} {current_value:>12.4f} {std_error:>12.4f}")

fig_path = os.path.join(BASE, "figures", "monte_carlo.png")
plt.savefig(fig_path, dpi = 200, bbox_inches = "tight")
plt.show()
