# Do 12-period EMA strategies work on futures? A 26-year, 13-market test

*Backtest research. Historical, hypothetical results; not a forecast and not investment advice (see the disclaimer at the end).*

## 1. Executive summary

- **One of 11 daily strategies passed all six pre-registered criteria: S06 Triple EMA (12/26/50 alignment), and only narrowly.** Its locked-test Sharpe is 0.35 against a 0.30 bar. It was positive in 12 of 13 markets and all 5 asset classes, with max drawdown −25% and Sharpe 0.22 even at severe costs. Because data and engine fixes were made after the test period had been seen (section 13), this pass is a **candidate to confirm on new data, not a proven edge**.
- **S05 EMA12/50 cross** missed by a hair (test Sharpe 0.29). **S04 EMA pullback** has the best test Sharpe (0.48), but 82% of its profit comes from 2 trades (silver and gold, 2025–26), with a −65% drawdown. Not recommended.
- **The 12-period EMA is too fast as a stand-alone daily signal.** S01 price/EMA cross, S02 slope and S08 ATR trend lose money in every split and at every cost level, even base costs: Sharpe −0.22 to −0.39 at base, −0.45 to −0.69 at moderate. They trade 150–200× their equity a year, and costs eat any edge.
- **Slower is better.** In the in-sample window (2001–15), almost every strategy improves as the fast EMA goes from 12 to 50–100. Walk-forward re-optimisation picked EMA 100 in most years for 7 of 11 strategies. Where the 12 works (S06, S05), it works as part of a slow, multi-EMA trend filter, not as a trigger.
- **S11 intraday opening-range breakout (NQ 5-min):** +0.15R per trade over its first 75 trades, then +0.015R over 328 trades in the test period. It decays to ~0; not robust.
- **Recommendation:** no capital deployment. Paper-trade S06 (and S05 as a control) on data after 23 Nov 2026 for ≥ 100 trades, with the same six criteria. A slow-EMA version of both is the natural next study (section 12).

## 2. Data and methodology

| | |
|---|---|
| Markets | ES, NQ, YM (equity) · CL, NG (energy) · GC, SI, HG (metals) · 6E, 6J, 6B (FX) · ZB, ZN (rates) |
| Daily data | Yahoo Finance front-month continuous `=F` series, Sep 2000 – 23 Nov 2026 (6,200–6,600 bars each) |
| Roll handling | Additive back-adjustment. Equity, FX and Treasuries roll on exact expiry calendars (≈4 rolls/yr); CL, NG and metals use the largest gap in a monthly window (approximate). See `docs/DATA.md` |
| Cleaning | Isolated spike-and-revert bars removed (4 in 26 years, e.g. 6J 2001-12-17 printed 10× too low). Real crashes kept (silver −31% on 2026-01-30). |
| Intraday (S11) | Dukascopy 1-min Nasdaq-100 CFD (proxy for NQ), 5-min bars. 566 sessions: 113 in-sample (Nov 2022 – Oct 2024, partial download) and 453 test (Nov 2024 – Nov 2026) |
| Splits | In-sample 2001–2015 · validation 2016–2020 · **locked test 2021–2026** · walk-forward 5-year train → 1-year test, 2006–2026 |

Every indicator at bar *t* uses only bars ≤ *t*. A unit test changes the future and checks that no past signal moves (`tests/test_engine.py`).

## 3. Strategy definitions
Full specification: `docs/STRATEGIES.md`.

S01 price/EMA cross · S02 EMA + 5-bar slope · S03 20-bar Donchian + EMA filter, 10-bar trailing stop · S04 pullback to EMA12 in an EMA12>EMA50 trend, swing stop · S05 EMA12/50 cross · S06 EMA 12/26/50 alignment · S07 MACD 12/26/9 + EMA filter · S08 EMA + rising ATR, 3-ATR chandelier · S09 20-bar breakout + rising EMA, 2-ATR trail · S10 ±2σ mean reversion around EMA12 with an EMA50/200 trend veto · S11 30-min opening-range breakout + 5-min EMA12 · S12 EMA12 trigger inside an EMA12-vs-EMA200 regime.

## 4. Backtesting assumptions
- Signals at the bar close; fills at the next bar's open.
- A stop already beyond the open fills at the open; otherwise at the stop level.
- No same-bar profit targets.
- A position held through a roll day pays one extra round turn.

## 5. Transaction-cost model
Per contract per side: **$2.50** commission and fees, plus slippage of 1 tick (ES, NQ, YM, GC, FX, Treasuries) or 2 ticks (CL, NG, SI, HG). Base = 1×, **moderate = 2× (used for every verdict)**, severe = 3× slippage.

## 6. Position-sizing framework
- `contracts = 0.5% × equity / (stop distance × point value)` on a $1M account, with **fractional contracts** for the main results, so the study measures the signals rather than account granularity.
- Whole-contract results at $1M are in the appendix. Rounding down skips 12–62% of entries there, because one ES, NQ, GC or SI contract often risks more than $5,000.
- Minimum stop = 0.5 ATR.
- Caps: 10% total open risk, 4% per asset class, margin ≤ 50% of equity at entry, daily loss limit 2% (no new entries the next day).
- A max-consecutive-loss rule (listed in the brief as "if applicable") was not implemented.

## 7. Performance results (EMA 12, moderate costs)

![equity](results/figures/equity_curves.png)

{{TABLE_VERDICTS}}

Failed criteria per strategy:

{{FAILED}}

Full metrics:

{{TABLE_FULL}}

Sharpe by period:

{{TABLE_SPLITS}}

Turnover and margin usage. Turnover is notional traded per year ÷ average equity, using |back-adjusted price| as an approximation. Margin is the sum of open positions' initial margin ÷ equity; it can exceed the 50% entry cap after equity falls.

{{TABLE_TURNOVER}}

S11 intraday (NQ 5-min, CFD proxy):

{{TABLE_S11}}

By market, asset class, calendar year and month: `results/by_sym.csv`, `results/by_cls.csv`, `results/by_year.csv`, `results/monthly/`.

![asset class](results/figures/by_asset_class.png)

## 8. Risk analysis
![drawdowns](results/figures/drawdowns.png)

- **The fast systems never recovered:** S01, S02 and S08 drew down 84–95%, a slow bleed from costs, not one crash.
- **S05 and S06 kept drawdowns near −25–27%.**
- **Trend-following profit is concentrated.** For every strategy, removing the best 1% of trades turns the total negative. That's normal for trend systems, which live on rare long trends. It means a few missed trades can erase years.
- **For S06, the top 2 trades are 28% of profit. For S04 they're 82%,** which is why S04 isn't recommended.
- **Strategy returns are correlated:** average pairwise correlation 0.43, max 0.93. Combining the trend variants adds little diversification.

## 9. Robustness testing
**Parameter sensitivity (in-sample 2001–15 only, as planned):**
- The 12 is never the best period.
- S01, S02 and S08 are negative across the whole 8–20 neighbourhood.
- S03 and S09 barely react to the EMA, because a 20-bar breakout is almost always above a rising EMA.
- S06 is stable from 12 to 100 (0.31–0.63).

The full-sample version (including the test period) is in the appendix.

![heatmap](results/figures/ema_heatmap.png)

**Cost stress:**
- Only S04, S05 and S06 stay positive at 3× slippage. S06 goes from Sharpe 0.36 at base costs to 0.22 at severe.
- S01 goes from −0.39 to −1.01.

![costs](results/figures/cost_stress.png)

**Regimes** (average R per trade, by the regime at entry; `results/by_trend.csv`, `by_vol.csv`, `by_market.csv`):
- S06 earns in sideways (+0.19R) and low-volatility (+0.15R) conditions, and loses in strongly trending entries (−0.16R): its entries come late in strong trends.
- S04 makes its money in trending conditions (+0.67R).
- S12's regime filter fails in sideways markets (−0.28R), exactly where it was meant to protect.

## 10. Walk-forward validation
Each year from 2006, the EMA period with the best Sharpe over the previous 5 years is applied to the next year only.

![walk-forward](results/figures/walk_forward.png)

- Walk-forward Sharpe is positive for 10 of 11 strategies (0.11–0.45; S10 −0.08), with S06 the highest at 0.45.
- This comes mostly from choosing **slow** EMAs: period 100 in 14–20 of 21 years for S01, S02, S03, S06, S08, S09 and S12, and 50 for S04 and S05.
- Caveat: each walk-forward year is cut from a full-period run with the chosen parameter, so the equity path inside a year is approximate.

## 11. Strategy rankings
1. **S06 Triple EMA: passed 6/6, narrowly.** The broadest edge, the lowest drawdown, cost-resilient. Confirm on new data before trusting it.
2. **S05 EMA12/50 cross: fragile, 5/6.** Test Sharpe 0.29 vs the 0.30 bar. A similar, slightly weaker profile.
3. **S04 EMA pullback: fragile, 5/6, not recommended.** Two trades make 82% of its profit, and its drawdown was −65%.
4. **Rejected:** S03, S07, S09, S12, S10, S08, S02, S01 (worst).
5. **S11 intraday: not robust.** Its edge decays to ~0 out of sample.

## 12. Implementation recommendations
- **Deploy nothing yet.** Paper-trade S06, with S05 as a control, from 24 Nov 2026 with exactly these rules, for ≥ 100 trades. Judge it on the same six criteria.
- **Next study** (pre-register before running): S06 and S05 with the fast EMA at 50 and an ATR-based exit, following the in-sample sensitivity.
- **Whole contracts need size.** At $1M, rounding skips 12–62% of entries. A real implementation needs micro contracts (MES, MNQ, MGC, SIL, M6E…) or a larger account, which changes costs.
- **Risk guide for any live version:**
  - 0.25–0.5% risk per trade, ≤ 2% open risk per asset class, stop = k × ATR (volatility sizing).
  - A hard 2% daily loss limit.
  - Stop a market after a drawdown of 3× its backtest worst; never add size after losses.
  - Review monthly against the backtest distribution: trades, win rate, average R.

## 13. Deviations from the plan (disclosed)
These were made **after the first full run, so after the 2021–26 test results had been seen**. They are data and engine fixes. **No strategy rule, parameter or pass criterion was changed.**

1. **Roll detection** changed from a z-score threshold, which missed most rolls, to exact expiry calendars for the quarterly contracts.
2. **Bad-tick filter** added after an audit of the largest trades found a 6J print 10× too low. It was then narrowed to spike-and-revert bars, because the first version also removed a real silver crash.
3. **The incomplete 24 Nov 2026 bar** was trimmed.
4. **A minimum stop of 0.5 ATR** was added: a gap next to a stop had produced an absurd position size (−71R).
5. **Fractional contracts** for the main results, with the whole-contract run moved to the appendix. This change **moved S06 from 4/6 to 6/6** criteria, which is why its pass is reported as narrow and to be confirmed.
6. **The sensitivity figure** uses the in-sample window, as the plan says. Criterion 5 was coded with full-sample Sharpe and is reported as run.

## 14. Limitations and risks
- **Data:** Yahoo front-month series are not exchange-grade. Roll detection for CL, NG and metals is approximate, there's no open interest, and CL's negative-price episode (April 2020) is only partly representable. A paid back-adjusted dataset could change individual results.
- **Costs:** estimated, not measured. Margins are approximate 2026 levels applied to the whole history.
- **S11** uses a CFD proxy with incomplete in-sample coverage (113 sessions).
- **Multiple testing:** 11 strategies × 6 periods × 3 cost levels. A few positive cells are expected by chance; S06's narrow pass should be read with that in mind.
- **Survivorship:** the universe is today's most liquid contracts, which slightly flatters history.

## 15. Disclaimer
This is hypothetical, backtested research for educational and portfolio purposes. Historical results do not guarantee future performance. Futures trading involves substantial risk of loss. Nothing here is investment advice.

## Appendix A: whole contracts on a $1M account

{{TABLE_INTEGER}}

## Appendix B: full-sample parameter sensitivity (includes the test period)

{{TABLE_FULLSENS}}

## Appendix C: reproduce
```bash
pip install -r requirements.txt
python scripts/run_all.py && python scripts/make_report.py && python scripts/build_report.py
pytest
```
Code: `src/casestudy/` (data, prep, indicators, strategies, engine, intraday, metrics, stats) · results: `results/` · figures: `results/figures/`.
