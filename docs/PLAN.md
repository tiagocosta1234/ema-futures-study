# Plan and pre-registration (written 24 Nov 2026, BEFORE any strategy was run)

## Pass criteria (fixed now, not changed after seeing results)
A strategy is **"robust"** only if ALL hold, net of **moderate** costs:
1. Out-of-sample (2021-01 → 2026-11) Sharpe > 0.3 at portfolio level.
2. Walk-forward out-of-sample windows: aggregate expectancy > 0.
3. Profit factor > 1.1 and ≥ 100 trades out of sample.
4. Positive in ≥ 60% of the 13 markets and in ≥ 3 of the 5 asset classes.
5. Parameter neighbourhood stable: EMA 10 and 20 versions keep ≥ 50% of the EMA-12 Sharpe.
6. Still positive under **severe** costs (otherwise "cost-fragile").
Anything else is reported as "rejected" or "fragile", with the reason. Negative results are reported, not hidden.

## Data splits
| Set | Period | Use |
|---|---|---|
| Train / in-sample | 2001-01 → 2015-12 | baselines, EMA-period sensitivity |
| Validation | 2016-01 → 2020-12 | choose among variants |
| **Test (locked)** | **2021-01 → 2026-11** | run ONCE with frozen rules |
| Walk-forward | rolling 5-year train → 1-year test, 2006 → 2026 | parameter choice only on the train window |

## Data (free sources, limitations disclosed)
- Daily: Yahoo Finance front-month continuous `=F` series, 2000/2002 → 2026 (`data/raw/daily/`, not committed). Not back-adjusted, no open interest. Roll days are detected (gap vs. the instrument's typical move on known roll weeks) and returns on those days are neutralised; documented in `docs/DATA.md`.
- Intraday (Strategy 11): Dukascopy 1-min CFDs for NQ/ES (and DAX, gold) resampled to 5-min; disclosed as CFD proxies.

## Costs (per contract, per side) — base / moderate / severe = 1× / 2× / 3× slippage
Commission + fees ≈ $2.50 per side. Base slippage: 1 tick (ES, NQ, YM, 6E, 6J, 6B, ZN, ZB, GC), 2 ticks (CL, SI, HG, NG).

## Phases (finite)
1. Data + roll handling + contract specs (tick, point value, margin) — tests.
2. Engine: next-open fills, sizing formula, portfolio risk caps, daily loss limit, margin check — tests (incl. a no-look-ahead test).
3. The 12 strategies as small functions — tests on toy series.
4. In-sample + validation runs, EMA sensitivity heatmaps.
5. Walk-forward + locked test + cost stress + regimes.
6. Report (`REPORT.md`) + figures + disclaimer.
