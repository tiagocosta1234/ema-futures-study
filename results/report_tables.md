| Strategy | Verdict | Criteria met | Full Sharpe | Full CAGR | Max DD | Test Sharpe | Test CAGR | Test trades | Walk-fwd Sharpe | Severe-cost Sharpe | Markets + | Classes + | Net P&L $k | Without top 1% trades $k |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S04 EMA pullback | **FRAGILE** | 5/6 | 0.16 | 1.2% | -61.4% | 0.57 | 12.8% | 553 | 0.30 | 0.13 | 7/13 | 2/5 | 528 | -2,096 (−25) |
| S06 Triple EMA | **FRAGILE** | 4/6 | 0.20 | 1.3% | -20.2% | 0.17 | 0.9% | 302 | 0.37 | 0.16 | 10/13 | 5/5 | 527 | -436 (−18) |
| S05 EMA12/50 cross | **FRAGILE** | 4/6 | 0.18 | 1.1% | -22.4% | 0.14 | 0.8% | 281 | 0.25 | 0.08 | 10/13 | 4/5 | 464 | -505 (−17) |
| S09 Vol breakout | **REJECTED** | 2/6 | 0.01 | -0.3% | -29.5% | -0.37 | -3.1% | 591 | 0.15 | -0.11 | 6/13 | 1/5 | 33 | -876 (−31) |
| S12 Regime switch | **REJECTED** | 1/6 | -0.09 | -0.9% | -26.3% | -0.06 | -0.5% | 805 | 0.19 | -0.38 | 7/13 | 3/5 | -139 | -1,292 (−53) |
| S03 Donchian+EMA | **REJECTED** | 1/6 | -0.03 | -0.8% | -35.9% | -0.20 | -2.0% | 489 | 0.17 | -0.11 | 5/13 | 1/5 | -79 | -997 (−28) |
| S08 ATR trend | **REJECTED** | 1/6 | -0.40 | -3.3% | -61.9% | -0.26 | -1.5% | 698 | 0.18 | -0.65 | 3/13 | 0/5 | -508 | -1,342 (−56) |
| S07 MACD+EMA | **REJECTED** | 1/6 | 0.08 | 0.3% | -32.6% | -0.37 | -3.6% | 970 | 0.29 | -0.16 | 7/13 | 3/5 | 217 | -1,215 (−50) |
| S10 Mean reversion | **REJECTED** | 0/6 | -0.25 | -1.1% | -27.5% | -0.17 | -0.6% | 284 | -0.17 | -0.44 | 6/13 | 2/5 | -217 | -383 (−17) |
| S02 EMA slope | **REJECTED** | 0/6 | -0.53 | -4.0% | -67.6% | -0.20 | -0.9% | 590 | 0.03 | -0.90 | 2/13 | 0/5 | -587 | -1,277 (−52) |
| S01 Price/EMA cross | **REJECTED** | 0/6 | -0.86 | -5.7% | -79.3% | -0.76 | -2.6% | 464 | -0.01 | -1.15 | 1/13 | 0/5 | -713 | -1,332 (−54) |

Failed criteria:

- **S04 EMA pullback**: 4 >= 60% markets and >= 3/5 classes positive
- **S06 Triple EMA**: 1 test Sharpe > 0.3; 3 test PF > 1.1 and >= 100 trades
- **S05 EMA12/50 cross**: 1 test Sharpe > 0.3; 3 test PF > 1.1 and >= 100 trades
- **S09 Vol breakout**: 1 test Sharpe > 0.3; 3 test PF > 1.1 and >= 100 trades; 4 >= 60% markets and >= 3/5 classes positive; 6 positive under severe costs
- **S12 Regime switch**: 1 test Sharpe > 0.3; 3 test PF > 1.1 and >= 100 trades; 4 >= 60% markets and >= 3/5 classes positive; 5 EMA 10 & 20 keep >= 50% of EMA-12 Sharpe; 6 positive under severe costs
- **S03 Donchian+EMA**: 1 test Sharpe > 0.3; 3 test PF > 1.1 and >= 100 trades; 4 >= 60% markets and >= 3/5 classes positive; 5 EMA 10 & 20 keep >= 50% of EMA-12 Sharpe; 6 positive under severe costs
- **S08 ATR trend**: 1 test Sharpe > 0.3; 3 test PF > 1.1 and >= 100 trades; 4 >= 60% markets and >= 3/5 classes positive; 5 EMA 10 & 20 keep >= 50% of EMA-12 Sharpe; 6 positive under severe costs
- **S07 MACD+EMA**: 1 test Sharpe > 0.3; 3 test PF > 1.1 and >= 100 trades; 4 >= 60% markets and >= 3/5 classes positive; 5 EMA 10 & 20 keep >= 50% of EMA-12 Sharpe; 6 positive under severe costs
- **S10 Mean reversion**: 1 test Sharpe > 0.3; 2 walk-forward positive; 3 test PF > 1.1 and >= 100 trades; 4 >= 60% markets and >= 3/5 classes positive; 5 EMA 10 & 20 keep >= 50% of EMA-12 Sharpe; 6 positive under severe costs
- **S02 EMA slope**: 1 test Sharpe > 0.3; 2 walk-forward positive; 3 test PF > 1.1 and >= 100 trades; 4 >= 60% markets and >= 3/5 classes positive; 5 EMA 10 & 20 keep >= 50% of EMA-12 Sharpe; 6 positive under severe costs
- **S01 Price/EMA cross**: 1 test Sharpe > 0.3; 2 walk-forward positive; 3 test PF > 1.1 and >= 100 trades; 4 >= 60% markets and >= 3/5 classes positive; 5 EMA 10 & 20 keep >= 50% of EMA-12 Sharpe; 6 positive under severe costs

| Strategy | Total return | CAGR | Max DD | DD days | Sharpe | Sortino | Calmar | PF | Win rate | Avg win $ | Avg loss $ | Expectancy $ | Exp. R | Trades/yr | Hold days | Exposure | Exp.-adj. return |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S01 Price/EMA cross | -78.5% | -5.7% | -79.3% | 9482 | -0.86 | -1.13 | -0.07 | 0.79 | 27.1% | 1,802 | -852 | -131 | -0.073 | 207 | 5.6 | 92.8% | -6.1% |
| S02 EMA slope | -65.9% | -4.0% | -67.6% | 9455 | -0.53 | -0.74 | -0.06 | 0.84 | 29.5% | 2,040 | -1,015 | -114 | -0.050 | 196 | 6.7 | 97.6% | -4.1% |
| S03 Donchian+EMA | -18.5% | -0.8% | -35.9% | 4926 | -0.03 | -0.05 | -0.02 | 0.99 | 33.6% | 5,707 | -2,934 | -28 | 0.004 | 108 | 14.6 | 99.4% | -0.8% |
| S04 EMA pullback | 37.1% | 1.2% | -61.4% | 5840 | 0.16 | 0.21 | 0.02 | 1.08 | 18.4% | 16,315 | -3,411 | 210 | 0.167 | 96 | 23.4 | 99.2% | 1.2% |
| S05 EMA12/50 cross | 33.5% | 1.1% | -22.4% | 2233 | 0.18 | 0.24 | 0.05 | 1.13 | 26.5% | 9,332 | -2,982 | 281 | 0.061 | 63 | 38.0 | 99.2% | 1.1% |
| S06 Triple EMA | 39.3% | 1.3% | -20.2% | 4312 | 0.20 | 0.29 | 0.06 | 1.13 | 31.2% | 8,216 | -3,305 | 292 | 0.075 | 69 | 30.8 | 99.2% | 1.3% |
| S07 MACD+EMA | 7.0% | 0.3% | -32.6% | 2432 | 0.08 | 0.11 | 0.01 | 1.02 | 35.1% | 5,572 | -2,941 | 43 | 0.009 | 190 | 11.2 | 99.6% | 0.3% |
| S08 ATR trend | -58.6% | -3.3% | -61.9% | 9455 | -0.40 | -0.55 | -0.05 | 0.89 | 29.3% | 2,429 | -1,133 | -90 | -0.037 | 215 | 6.6 | 97.9% | -3.4% |
| S09 Vol breakout | -6.4% | -0.3% | -29.5% | 2880 | 0.01 | 0.02 | -0.01 | 1.01 | 35.9% | 5,408 | -3,017 | 11 | 0.012 | 118 | 12.3 | 99.3% | -0.3% |
| S10 Mean reversion | -24.7% | -1.1% | -27.5% | 9533 | -0.25 | -0.30 | -0.04 | 0.91 | 56.5% | 2,180 | -3,118 | -127 | -0.027 | 65 | 6.3 | 76.8% | -1.4% |
| S12 Regime switch | -21.0% | -0.9% | -26.3% | 9146 | -0.09 | -0.12 | -0.03 | 0.97 | 28.9% | 3,464 | -1,448 | -26 | -0.004 | 202 | 6.1 | 95.5% | -0.9% |

| Strategy | In-sample 2001–15 | Validation 2016–20 | Test 2021–26 |
|---|---|---|---|
| S01 Price/EMA cross | -0.99 | -0.82 | -0.76 |
| S02 EMA slope | -0.70 | -0.36 | -0.20 |
| S03 Donchian+EMA | 0.02 | -0.08 | -0.20 |
| S04 EMA pullback | -0.04 | 0.07 | 0.57 |
| S05 EMA12/50 cross | 0.20 | 0.21 | 0.14 |
| S06 Triple EMA | 0.29 | -0.10 | 0.17 |
| S07 MACD+EMA | 0.12 | 0.38 | -0.37 |
| S08 ATR trend | -0.64 | 0.04 | -0.26 |
| S09 Vol breakout | 0.09 | 0.17 | -0.37 |
| S10 Mean reversion | -0.16 | -0.27 | -0.17 |
| S12 Regime switch | -0.09 | -0.13 | -0.06 |

| S11 (NQ 5-min) | Split | Trades | Win | Avg R | t | P&L $ | PF |
|---|---|---|---|---|---|---|---|
| base | in_sample | 75 | 52.0% | 0.156 | 1.53 | 50,738 | 1.63 |
| base | test | 328 | 41.5% | 0.019 | 0.44 | 20,235 | 1.07 |
| base | all | 403 | 43.4% | 0.045 | 1.11 | 70,973 | 1.19 |
| moderate | in_sample | 75 | 52.0% | 0.149 | 1.46 | 48,398 | 1.59 |
| moderate | test | 328 | 41.5% | 0.015 | 0.35 | 15,415 | 1.05 |
| moderate | all | 403 | 43.4% | 0.040 | 1.00 | 63,813 | 1.17 |
| severe | in_sample | 75 | 52.0% | 0.142 | 1.39 | 46,058 | 1.55 |
| severe | test | 328 | 41.2% | 0.011 | 0.26 | 10,595 | 1.04 |
| severe | all | 403 | 43.2% | 0.036 | 0.88 | 56,653 | 1.15 |

| S11 EMA period | Trades | Avg R | t |
|---|---|---|---|
| 8 | 403 | 0.044 | 1.09 |
| 10 | 403 | 0.044 | 1.10 |
| 12 | 403 | 0.040 | 1.00 |
| 20 | 398 | 0.039 | 0.99 |
| 50 | 390 | 0.028 | 0.70 |
| 100 | 376 | 0.021 | 0.52 |