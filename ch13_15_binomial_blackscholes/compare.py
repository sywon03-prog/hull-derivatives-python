from black_scholes import black_scholes
from binomial import binomial
from binomial import binomial_backward
import matplotlib.pyplot as plt
import scienceplots    
import numpy as np

plt.style.use(['science', 'no-latex'])



def bs_call_graph(S, K, r, sigma, T, option_type):
    hist_bc = []
    hist_intrinsic = []
    hist_Lowest = []
    for i in range(20, 60, 2):
        hist_bc.append(black_scholes(S=i, K=K, r=r, sigma=sigma, T=T, option_type=option_type))
        hist_intrinsic.append(np.maximum(i - K, 0))
        hist_Lowest.append(np.maximum(i - K*np.exp(-r*T), 0))
    return hist_bc, hist_intrinsic, hist_Lowest

def bs_put_graph(S, K, r, sigma, T, option_type):
    hist_bp = []
    hist_intrinsic = []
    hist_Lowest = []
    for i in range(20, 60, 2):
        hist_bp.append(black_scholes(S=i, K=K, r=r, sigma=sigma, T=T, option_type=option_type))
        hist_intrinsic.append(np.maximum(K - i, 0))
        hist_Lowest.append(np.maximum(K*np.exp(-r*T) - i, 0))
    return hist_bp, hist_intrinsic, hist_Lowest

def binomial_vs_black_scholes(S, K, r, sigma, T, option_type) :
    hist_bi = []
    for i in range(1,201,1) :
        hist_bi.append(binomial_backward(S, K, r, sigma, T,i, option_type))
    bs_price = black_scholes(S, K, r, sigma, T, option_type)
    return hist_bi, bs_price

bc_hist, bc_intrinsic, bc_Lowest = bs_call_graph(S=42, K=40, r=0.10, sigma=0.20, T=0.5, option_type="call")
bp_hist, bp_intrinsic, bp_Lowest = bs_put_graph(S=42, K=40, r=0.10, sigma=0.20, T=0.5, option_type="put")

s = range(20, 60, 2)
fig, axes = plt.subplots(1, 2, figsize=(12, 5)) 


axes[0].plot(s, bc_hist, color='red', label='Call price')
axes[0].plot(s, bc_intrinsic, ls='--', label='Intrinsic value')
axes[0].plot(s, bc_Lowest, ls=':', label='Lower bound')
axes[0].set_title('European Call')
axes[0].set_xlabel('Initial stock price $S_0$')
axes[0].set_ylabel('Value')
axes[0].legend()


axes[1].plot(s, bp_hist, color='red', label='Put price')
axes[1].plot(s, bp_intrinsic, ls='--', label='Intrinsic value')
axes[1].plot(s, bp_Lowest, ls=':', label='Lower bound')
axes[1].set_title('European Put')
axes[1].set_xlabel('Initial stock price $S_0$')
axes[1].legend()

fig.tight_layout()
fig.savefig('figures/price_vs_S.png', dpi=300, bbox_inches='tight')

hist_bi, bs_price = binomial_vs_black_scholes(S=42, K=40, r=0.10, sigma=0.20, T=0.5, option_type="call")
fig, axes = plt.subplots(figsize=(10,10)) 
n = range(1,201,1)
axes.plot(n,hist_bi,color = 'black', label = "Binomial Model")
axes.axhline(bs_price,color = 'red', label = "Black Scholes",ls = "--")
axes.set_xlabel("Number of time steps $n$")
axes.set_ylabel('Call price')
axes.legend()

fig.savefig('figures/convergence.png', dpi=300, bbox_inches='tight')
plt.show()