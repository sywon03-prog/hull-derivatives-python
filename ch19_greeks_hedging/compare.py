from Delta import Delta
from Gamma import Gamma
from Theta import Theta
import matplotlib.pyplot as plt
import scienceplots
import numpy as np
import os

plt.style.use(['science', 'no-latex'])

FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures')
os.makedirs(FIG_DIR, exist_ok=True)



def greek_vs_T(greek, S, K, r, sigma, q, option_type):
    hist = []
    for t in T_range:
        if greek == "Gamma":
            hist.append(Gamma(S=S, K=K, r=r, sigma=sigma, T=t, q=q))
        elif greek == "Theta":
            hist.append(Theta(S=S, K=K, r=r, sigma=sigma, T=t, q=q, option_type=option_type))
        else:
            hist.append(Delta(S=S, K=K, r=r, sigma=sigma, T=t, q=q, option_type=option_type))
    return hist

def greek_vs_S(greek, K, r, sigma, T, q, option_type):
    hist = []
    for s in S_range:
        if greek == "Gamma":
            hist.append(Gamma(S=s, K=K, r=r, sigma=sigma, T=T, q=q))
        elif greek == "Theta":
            hist.append(Theta(S=s, K=K, r=r, sigma=sigma, T=T, q=q, option_type=option_type))
        else:
            hist.append(Delta(S=s, K=K, r=r, sigma=sigma, T=T, q=q, option_type=option_type))
    return hist

T_range = np.linspace(0.01, 10, 200)
S_range = np.linspace(1, 120, 200)

# Delta
itm_hist = greek_vs_T("Delta", S=60, K=50, r=0.05, sigma=0.20, q=0.0, option_type="call")
atm_hist = greek_vs_T("Delta", S=50, K=50, r=0.05, sigma=0.20, q=0.0, option_type="call")
otm_hist = greek_vs_T("Delta", S=40, K=50, r=0.05, sigma=0.20, q=0.0, option_type="call")
s_hist = greek_vs_S("Delta", K=50, r=0.05, sigma=0.20, T=20/52, q=0.0, option_type="call")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].plot(T_range, itm_hist, ls='--', label='ITM')
axes[0].plot(T_range, atm_hist, label='ATM')
axes[0].plot(T_range, otm_hist, ls='-.', label='OTM')
axes[0].set_title('Delta vs Time to maturity')
axes[0].set_xlabel('Time to maturity $T$')
axes[0].set_ylabel('Call Delta')
axes[0].legend()

axes[1].plot(S_range, s_hist)
axes[1].set_title('Delta vs Stock price')
axes[1].set_xlabel('Stock price $S$')

fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, 'delta.png'), dpi=300, bbox_inches='tight')

# Gamma
itm_hist = greek_vs_T("Gamma", S=60, K=50, r=0.05, sigma=0.20, q=0.0, option_type="call")
atm_hist = greek_vs_T("Gamma", S=50, K=50, r=0.05, sigma=0.20, q=0.0, option_type="call")
otm_hist = greek_vs_T("Gamma", S=40, K=50, r=0.05, sigma=0.20, q=0.0, option_type="call")
s_hist = greek_vs_S("Gamma", K=50, r=0.05, sigma=0.20, T=20/52, q=0.0, option_type="call")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].plot(T_range, itm_hist, ls='--', label='ITM')
axes[0].plot(T_range, atm_hist, label='ATM')
axes[0].plot(T_range, otm_hist, ls='-.', label='OTM')
axes[0].set_title('Gamma vs Time to maturity')
axes[0].set_xlabel('Time to maturity $T$')
axes[0].set_ylabel('Call Gamma')
axes[0].legend()

axes[1].plot(S_range, s_hist)
axes[1].set_title('Gamma vs Stock price')
axes[1].set_xlabel('Stock price $S$')

fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, 'gamma.png'), dpi=300, bbox_inches='tight')

# Theta
itm_hist = greek_vs_T("Theta", S=60, K=50, r=0.05, sigma=0.20, q=0.0, option_type="call")
atm_hist = greek_vs_T("Theta", S=50, K=50, r=0.05, sigma=0.20, q=0.0, option_type="call")
otm_hist = greek_vs_T("Theta", S=40, K=50, r=0.05, sigma=0.20, q=0.0, option_type="call")
s_hist = greek_vs_S("Theta", K=50, r=0.05, sigma=0.20, T=20/52, q=0.0, option_type="call")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].plot(T_range, itm_hist, ls='--', label='ITM')
axes[0].plot(T_range, atm_hist, label='ATM')
axes[0].plot(T_range, otm_hist, ls='-.', label='OTM')
axes[0].set_title('Theta vs Time to maturity')
axes[0].set_xlabel('Time to maturity $T$')
axes[0].set_ylabel('Call Theta')
axes[0].legend()

axes[1].plot(S_range, s_hist)
axes[1].set_title('Theta vs Stock price')
axes[1].set_xlabel('Stock price $S$')

fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, 'theta.png'), dpi=300, bbox_inches='tight')
plt.show()
