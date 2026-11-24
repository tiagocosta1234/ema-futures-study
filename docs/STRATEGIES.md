# Strategy specification (as implemented in `src/casestudy/strategies.py` and `intraday.py`)

Common to all daily strategies: `n` = fast EMA period (12 by default; the sweep uses 8/10/12/20/50/100). Signals at the close of bar *t*, executed at the open of *t+1*. Default initial stop = 2 × ATR(14) from the signal bar's close; minimum stop 0.5 × ATR. Trailing stops only move in the trade's favour. An opposite entry signal reverses the position.

| # | Entry long (short = mirror) | Exit | Stop |
|---|---|---|---|
| S01 | close crosses above EMA(n) | opposite cross | 2 ATR |
| S02 | close > EMA(n) and EMA(n) − EMA(n)[5 bars ago] > 0 (first bar of the condition) | close < EMA or slope ≤ 0 | 2 ATR |
| S03 | close > highest high of the prior 20 bars and close > EMA(n) | trailing stop = lowest low of 10 bars | 2 ATR initial |
| S04 | EMA(n) > EMA(50) (EMA 200 if n ≥ 50), low ≤ EMA(n) and close > EMA(n) | trend flips | lowest low of 5 bars (swing) |
| S05 | EMA(n) crosses above EMA(50) (200 if n ≥ 50) | opposite cross | 3 ATR |
| S06 | EMA(n) > EMA(26/12·n) > EMA(50/12·n) (first bar) | EMA(n) crosses below EMA(26/12·n) | 3 ATR |
| S07 | MACD = EMA(n) − EMA(26/12·n) crosses above its 9-EMA signal and close > EMA(n) | opposite MACD/signal cross | 2 ATR |
| S08 | close > EMA(n) and ATR(14) > ATR(14) 5 bars ago (first bar) | close < EMA(n) | 2 ATR initial, 3 ATR chandelier trail |
| S09 | close > highest high of prior 20 bars and EMA(n) rising | opposite breakout | 2 ATR initial, 2 ATR trail |
| S10 | z = (close − EMA(n)) / 20-bar std of that distance < −2, unless strongly bearish (EMA50 < EMA200 and EMA50 falling over 20 bars) | close ≥ EMA(n) | 2 ATR |
| S11 | 5-min close > 09:30–10:00 high and > 5-min EMA(n), from 10:00 NY; one trade/day | 2 ATR(5-min) trail, flat at 15:55 | fixed = opening-range height |
| S12 | close crosses above EMA(n) while EMA(n) > EMA(200) | close crosses below EMA(n) | 2 ATR |

Volatility-based sizing (S08, S09 and all others) comes from the sizing rule itself: contracts = risk ÷ (stop distance × point value), with stops in ATR units.
