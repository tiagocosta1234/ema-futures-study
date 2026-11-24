| Strategy | Verdict | Criteria met | Full Sharpe | Full CAGR | Max DD | Test Sharpe | Test CAGR | Test trades | Walk-fwd Sharpe | Severe-cost Sharpe | Markets + | Classes + | Net P&L $k | Without top 1% trades $k |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S06 Triple EMA | **ROBUST** | 6/6 | 0.29 | 2.6% | -25.2% | 0.35 | 3.5% | 479 | 0.45 | 0.22 | 12/13 | 5/5 | 1,133 | -543 (−21) |
| S04 EMA pullback | **FRAGILE** | 5/6 | 0.17 | 1.2% | -65.1% | 0.48 | 10.1% | 569 | 0.30 | 0.09 | 9/13 | 4/5 | 533 | -2,342 (−26) |
| S05 EMA12/50 cross | **FRAGILE** | 5/6 | 0.22 | 1.9% | -26.9% | 0.29 | 2.9% | 454 | 0.31 | 0.16 | 10/13 | 5/5 | 813 | -815 (−21) |
| S03 Donchian+EMA | **REJECTED** | 2/6 | 0.09 | 0.3% | -40.0% | -0.06 | -1.8% | 746 | 0.23 | -0.01 | 6/13 | 2/5 | 218 | -1,305 (−32) |
| S07 MACD+EMA | **REJECTED** | 2/6 | 0.09 | 0.3% | -39.0% | -0.24 | -4.0% | 1293 | 0.31 | -0.07 | 8/13 | 4/5 | 255 | -1,471 (−55) |
| S09 Vol breakout | **REJECTED** | 2/6 | 0.08 | 0.3% | -36.4% | -0.36 | -4.6% | 813 | 0.22 | -0.04 | 5/13 | 2/5 | 198 | -1,145 (−35) |
| S12 Regime switch | **REJECTED** | 1/6 | -0.11 | -1.6% | -41.4% | -0.06 | -1.2% | 1555 | 0.23 | -0.33 | 6/13 | 2/5 | -265 | -1,744 (−66) |
| S08 ATR trend | **REJECTED** | 1/6 | -0.45 | -6.4% | -83.9% | -0.48 | -6.9% | 2048 | 0.27 | -0.67 | 3/13 | 0/5 | -738 | -1,943 (−89) |
| S02 EMA slope | **REJECTED** | 1/6 | -0.49 | -7.4% | -87.9% | -0.54 | -8.3% | 2295 | 0.15 | -0.75 | 0/13 | 0/5 | -785 | -1,965 (−99) |
| S01 Price/EMA cross | **REJECTED** | 1/6 | -0.69 | -10.5% | -94.9% | -0.67 | -10.5% | 3199 | 0.11 | -1.01 | 1/13 | 0/5 | -861 | -2,112 (−138) |
| S10 Mean reversion | **REJECTED** | 0/6 | -0.14 | -1.0% | -32.9% | 0.16 | 0.7% | 542 | -0.08 | -0.29 | 4/13 | 1/5 | -189 | -415 (−22) |

Failed criteria:

- **S06 Triple EMA**: none
- **S04 EMA pullback**: 6 positive under severe costs
- **S05 EMA12/50 cross**: 1 test Sharpe > 0.3
- **S03 Donchian+EMA**: 1 test Sharpe > 0.3; 3 test PF > 1.1 and >= 100 trades; 4 >= 60% markets and >= 3/5 classes positive; 6 positive under severe costs
- **S07 MACD+EMA**: 1 test Sharpe > 0.3; 3 test PF > 1.1 and >= 100 trades; 5 EMA 10 & 20 keep >= 50% of EMA-12 Sharpe; 6 positive under severe costs
- **S09 Vol breakout**: 1 test Sharpe > 0.3; 3 test PF > 1.1 and >= 100 trades; 4 >= 60% markets and >= 3/5 classes positive; 6 positive under severe costs
- **S12 Regime switch**: 1 test Sharpe > 0.3; 3 test PF > 1.1 and >= 100 trades; 4 >= 60% markets and >= 3/5 classes positive; 5 EMA 10 & 20 keep >= 50% of EMA-12 Sharpe; 6 positive under severe costs
- **S08 ATR trend**: 1 test Sharpe > 0.3; 3 test PF > 1.1 and >= 100 trades; 4 >= 60% markets and >= 3/5 classes positive; 5 EMA 10 & 20 keep >= 50% of EMA-12 Sharpe; 6 positive under severe costs
- **S02 EMA slope**: 1 test Sharpe > 0.3; 3 test PF > 1.1 and >= 100 trades; 4 >= 60% markets and >= 3/5 classes positive; 5 EMA 10 & 20 keep >= 50% of EMA-12 Sharpe; 6 positive under severe costs
- **S01 Price/EMA cross**: 1 test Sharpe > 0.3; 3 test PF > 1.1 and >= 100 trades; 4 >= 60% markets and >= 3/5 classes positive; 5 EMA 10 & 20 keep >= 50% of EMA-12 Sharpe; 6 positive under severe costs
- **S10 Mean reversion**: 1 test Sharpe > 0.3; 2 walk-forward positive; 3 test PF > 1.1 and >= 100 trades; 4 >= 60% markets and >= 3/5 classes positive; 5 EMA 10 & 20 keep >= 50% of EMA-12 Sharpe; 6 positive under severe costs

| Strategy | Total return | CAGR | Max DD | DD days | Sharpe | Sortino | Calmar | PF | Win rate | Avg win $ | Avg loss $ | Expectancy $ | Exp. R | Trades/yr | Hold days | Exposure | Exp.-adj. return |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S01 Price/EMA cross | -94.5% | -10.5% | -94.9% | 9554 | -0.69 | -1.04 | -0.11 | 0.84 | 28.2% | 1,188 | -554 | -62 | -0.042 | 527 | 5.8 | 99.8% | -10.5% |
| S02 EMA slope | -86.8% | -7.4% | -87.9% | 9455 | -0.49 | -0.72 | -0.08 | 0.86 | 30.0% | 1,664 | -828 | -80 | -0.038 | 376 | 6.7 | 99.7% | -7.4% |
| S03 Donchian+EMA | 7.2% | 0.3% | -40.0% | 4926 | 0.09 | 0.12 | 0.01 | 1.02 | 34.7% | 8,205 | -4,249 | 67 | 0.015 | 124 | 14.9 | 99.6% | 0.3% |
| S04 EMA pullback | 36.5% | 1.2% | -65.1% | 6721 | 0.17 | 0.22 | 0.02 | 1.07 | 19.3% | 17,367 | -3,891 | 208 | 0.163 | 98 | 24.7 | 99.2% | 1.2% |
| S05 EMA12/50 cross | 63.4% | 1.9% | -26.9% | 4116 | 0.22 | 0.30 | 0.07 | 1.13 | 27.4% | 12,607 | -4,218 | 394 | 0.077 | 79 | 39.0 | 99.2% | 1.9% |
| S06 Triple EMA | 94.4% | 2.6% | -25.2% | 2657 | 0.29 | 0.39 | 0.10 | 1.16 | 31.6% | 12,062 | -4,809 | 529 | 0.084 | 82 | 31.5 | 99.2% | 2.6% |
| S07 MACD+EMA | 8.5% | 0.3% | -39.0% | 2496 | 0.09 | 0.13 | 0.01 | 1.02 | 35.2% | 6,628 | -3,522 | 46 | 0.011 | 211 | 11.2 | 99.6% | 0.3% |
| S08 ATR trend | -82.1% | -6.4% | -83.9% | 9455 | -0.45 | -0.66 | -0.08 | 0.88 | 29.6% | 1,975 | -948 | -83 | -0.034 | 341 | 6.6 | 99.7% | -6.4% |
| S09 Vol breakout | 7.0% | 0.3% | -36.4% | 4319 | 0.08 | 0.12 | 0.01 | 1.02 | 36.6% | 7,522 | -4,246 | 57 | 0.015 | 131 | 12.5 | 99.5% | 0.3% |
| S10 Mean reversion | -22.4% | -1.0% | -32.9% | 9533 | -0.14 | -0.17 | -0.03 | 0.95 | 57.6% | 2,594 | -3,725 | -86 | -0.014 | 84 | 6.2 | 84.1% | -1.1% |
| S12 Regime switch | -34.6% | -1.6% | -41.4% | 9146 | -0.11 | -0.15 | -0.04 | 0.96 | 29.7% | 3,585 | -1,573 | -40 | -0.006 | 253 | 6.2 | 96.7% | -1.7% |

| Strategy | In-sample 2001–15 | Validation 2016–20 | Test 2021–26 |
|---|---|---|---|
| S01 Price/EMA cross | -0.83 | -0.41 | -0.67 |
| S02 EMA slope | -0.66 | -0.05 | -0.54 |
| S03 Donchian+EMA | 0.16 | 0.01 | -0.06 |
| S04 EMA pullback | -0.05 | 0.27 | 0.48 |
| S05 EMA12/50 cross | 0.20 | 0.20 | 0.29 |
| S06 Triple EMA | 0.31 | 0.07 | 0.35 |
| S07 MACD+EMA | 0.09 | 0.41 | -0.24 |
| S08 ATR trend | -0.69 | 0.08 | -0.48 |
| S09 Vol breakout | 0.21 | 0.19 | -0.36 |
| S10 Mean reversion | -0.15 | -0.18 | 0.16 |
| S12 Regime switch | -0.18 | 0.04 | -0.06 |

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

| Strategy | Turnover (x equity / yr) | Avg margin / equity | Max margin / equity |
|---|---|---|---|
| S01 Price/EMA cross | 200.6 | 36.8% | 117.8% |
| S02 EMA slope | 156.8 | 31.0% | 84.5% |
| S03 Donchian+EMA | 57.7 | 22.3% | 63.5% |
| S04 EMA pullback | 81.7 | 33.7% | 90.7% |
| S05 EMA12/50 cross | 24.2 | 23.2% | 71.3% |
| S06 Triple EMA | 25.5 | 20.6% | 68.6% |
| S07 MACD+EMA | 100.3 | 27.5% | 88.1% |
| S08 ATR trend | 146.9 | 29.1% | 86.7% |
| S09 Vol breakout | 61.3 | 20.1% | 63.4% |
| S10 Mean reversion | 38.0 | 6.6% | 62.2% |
| S12 Regime switch | 115.6 | 20.4% | 83.4% |

| Strategy (whole contracts, $1M) | Sharpe | CAGR | Trades | Entries skipped (0 contracts) |
|---|---|---|---|---|
| S01 Price/EMA cross | -0.86 | -5.7% | 5424 | 9004 (62.4%) |
| S02 EMA slope | -0.53 | -4.0% | 5156 | 4861 (48.5%) |
| S03 Donchian+EMA | -0.03 | -0.8% | 2848 | 1671 (37.0%) |
| S04 EMA pullback | 0.16 | 1.2% | 2517 | 673 (21.1%) |
| S05 EMA12/50 cross | 0.18 | 1.1% | 1653 | 433 (20.8%) |
| S06 Triple EMA | 0.20 | 1.3% | 1803 | 348 (16.2%) |
| S07 MACD+EMA | 0.08 | 0.3% | 4983 | 654 (11.6%) |
| S08 ATR trend | -0.40 | -3.3% | 5647 | 4497 (44.3%) |
| S09 Vol breakout | 0.01 | -0.3% | 3086 | 1417 (31.5%) |
| S10 Mean reversion | -0.25 | -1.1% | 1718 | 942 (35.4%) |
| S12 Regime switch | -0.09 | -0.9% | 5304 | 1389 (20.8%) |

| Full-sample Sharpe (includes the test period) | EMA 8 | EMA 10 | EMA 12 | EMA 20 | EMA 50 | EMA 100 |
|---|---|---|---|---|---|---|
| S01 Price/EMA cross | -0.92 | -0.79 | -0.69 | -0.49 | -0.05 | 0.18 |
| S02 EMA slope | -0.63 | -0.54 | -0.49 | -0.32 | 0.07 | 0.24 |
| S03 Donchian+EMA | 0.09 | 0.09 | 0.09 | 0.09 | 0.10 | 0.17 |
| S04 EMA pullback | 0.33 | 0.28 | 0.17 | 0.26 | 0.51 | 0.35 |
| S05 EMA12/50 cross | 0.20 | 0.22 | 0.22 | 0.33 | 0.51 | 0.42 |
| S06 Triple EMA | 0.12 | 0.26 | 0.29 | 0.39 | 0.49 | 0.57 |
| S07 MACD+EMA | -0.15 | -0.01 | 0.09 | 0.39 | 0.46 | 0.33 |
| S08 ATR trend | -0.68 | -0.58 | -0.45 | -0.21 | 0.16 | 0.24 |
| S09 Vol breakout | 0.08 | 0.08 | 0.08 | 0.08 | 0.09 | 0.17 |
| S10 Mean reversion | 0.10 | -0.02 | -0.14 | -0.06 | -0.02 | -0.14 |
| S12 Regime switch | -0.25 | -0.16 | -0.11 | 0.08 | 0.31 | 0.41 |