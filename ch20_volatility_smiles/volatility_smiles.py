import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from bs import black_scholes
from Vega import Vega
import scienceplots
import os
BASE = os.path.dirname(os.path.abspath(__file__))

tk = yf.Ticker("QQQ")

S = tk.history(period = "1d")["Close"].iloc[-1]
today = pd.Timestamp.today().normalize()

# 만기일 계산
exps = pd.Series(pd.to_datetime(tk.options))
days = (exps - today).dt.days

#1달,3달,6달과 가장 가까운 만기일 선택
targets = [30, 90, 180]
picked = [exps[(days - d).abs().idxmin()].strftime("%Y-%m-%d") for d in targets]

rows = []
for exp in picked :
    ch = tk.option_chain(exp)
    T = (pd.Timestamp(exp) - today).days / 365
    for typ, df in [("call", ch.calls), ("put", ch.puts)] :
        rows.append(df.assign(expiry=exp, T=T, type=typ))

#만기별 풋,콜을 담은 rows 세로로 붙이고, 두 열 추가(QQQ가격 S, 중앙 호가 mid)
data = pd.concat(rows, ignore_index=True)
data["S"] = S
data["mid"] = (data["bid"] + data["ask"]) / 2
data.to_csv(os.path.join(BASE, "qqq_chain.csv"), index=False)
print(data)
print(picked, f"S = {S:.2f}")

#무위험 수익률
r = 0.04

# 풋-콜 패리티로 만기별 q 역산 (정제 전, 등가격에 가장 가까운 콜, 풋 한 쌍으로 구함. )
calls = data[data["type"] == "call"][["expiry", "T", "strike", "mid"]]
puts = data[data["type"] == "put"][["expiry", "T", "strike", "mid"]]
pairs = calls.merge(puts, on=["expiry", "T", "strike"], suffixes=("_c", "_p"))

q_by_expiry = {}
for exp in picked :
    sub = pairs[pairs["expiry"] == exp]
    row = sub.iloc[(sub["strike"] - S).abs().argmin()]
    T = row["T"]
    S_eqT = row["mid_c"] - row["mid_p"] + row["strike"] * np.exp(-r * T)
    q_by_expiry[exp] = -np.log(S_eqT / S) / T

data["q"] = data["expiry"].map(q_by_expiry)
print(q_by_expiry)

# 데이터 정제
otm = ((data["type"] == "call") & (data["strike"] > S)) | ((data["type"] == "put") & (data["strike"] < S))
data = data[otm]

data = data[(data["bid"] > 0) & (data["openInterest"] > 0)]

data = data[(data["strike"] >= 0.85 * S) & (data["strike"] <= 1.15 * S)]

data = data.sort_values(["expiry", "strike"]).reset_index(drop=True)

def implied_vol_newton(price, S, K, r, T, type, q, sigma0 =0.3, max_iter = 100) :
    sigma = sigma0
    for _ in range(max_iter) :
        diff = black_scholes(S, K, r, sigma, T, q, option_type = type) - price
        # 이론값 - 시장가격 차이가 매우 적어지면 비교적 정확한 IV가 찾아졌다고 판단 후 종료
        if abs(diff) < 1e-8 :
            return sigma
        v = Vega(S, K, r, sigma, T, q)
        if v < 1e-10 :
            return np.nan
        #뉴턴-랩슨법으로 b-l값을 시장가격에 수렴시키며 sigma 업데이트함.
        sigma = sigma - diff / v
        # 음수로 튀면 작은 값으로 되돌림
        if sigma <= 0:           
            sigma = 1e-4
    return np.nan

data["iv"] = data.apply(
    lambda row: implied_vol_newton(row["mid"], row["S"], row["strike"], r, row["T"], row["type"], row["q"]),
    axis=1,
)

print(data["iv"])

plt.style.use(['science', 'no-latex'])

fig, ax = plt.subplots(figsize=(8, 5))
for exp, g in data.groupby("expiry"):
    ax.plot(g["strike"] / g["S"], g["iv"], label=f"{exp} (T={g['T'].iloc[0]:.2f})")
ax.axvline(1.0, color="gray", ls="--", lw=0.8)
ax.set_xlabel("Moneyness $K/S_0$")
ax.set_ylabel("Implied volatility")
ax.legend()

fig.tight_layout()
fig_path = os.path.join(BASE, "figures", "volatility_smiles.png")
fig.savefig(fig_path, dpi=300, bbox_inches="tight")
plt.show()