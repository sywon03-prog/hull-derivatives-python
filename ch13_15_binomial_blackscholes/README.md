## 설명

이항모형, 위너과정과 이토정리, 블랙숄즈방정식 부분을 읽고 두가지를 파이썬으로 구현했다.

1. 1기간 이항모형,다기간 이항모형 
2. 블랙-숄즈 옵션가격결정모형

구현 후, 두가지를 그래프로 확인해봤다.

1. 초기 주가에 따른 옵션 가격의 변화
2. 이항 모형에서 기간 수 n에 따른 블랙-숄즈 모형으로의 수렴

### Option value vs Initial stock price S 
![price vs S](figures/price_vs_S.png)

무배당의 경우, 
- call은 항상 Intrinsic value가 Lower bound 아래 있으므로, 조기 행사가 불리하고,

- put은 Intrinsic value가 Lower bound보다 위에 있으므로, put 가치가 Intrinsic value 보다 작아질 수 있다. 이 경우 조기행사가 유리하다.


### 이항 모형의 Black-scholes 수렴
![Convergence](figures/convergence.png)

Hull 13장에 따르면 이항모형은 기하 브라운 운동의 이산 근사이므로,
$n \to \infty$일 때 Black-Scholes 가격으로 수렴한다. 이를 직접 확인했다.

- n이 커질수록 이항모형 가격이 Black-scholes 가격으로 수렴한다.
- 수렴 과정에서 가격은 n의 짝,홀에 따라 지그재그로 진동한다.

