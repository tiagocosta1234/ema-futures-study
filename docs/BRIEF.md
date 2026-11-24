# Case study brief (as received, 24 Nov 2026)

**Evaluation of 12 EMA-based trading strategies on futures markets.** Determine whether a 12-period EMA adds value as a standalone signal, trend filter, entry trigger, exit mechanism or risk-management component, with consistent assumptions, realistic execution and out-of-sample validation.

Universe: ES, NQ, YM · CL, NG · GC, SI, HG · 6E, 6J, 6B · ZB, ZN. Daily bars (primary, 10–15+ years), 5/15-min bars (secondary, intraday Strategy 11).

Strategies: 1 Price/EMA12 cross · 2 EMA12 slope filter · 3 Donchian 20 + EMA12 filter · 4 EMA12 pullback · 5 EMA12/50 cross · 6 Triple EMA 12/26/50 · 7 MACD 12/26/9 + EMA12 filter · 8 ATR trend (EMA12 + rising ATR14) · 9 Volatility-adjusted 20-bar breakout · 10 EMA12 mean reversion (±2σ) · 11 Opening-range (30 min) breakout + EMA12 (intraday) · 12 Regime switch EMA12 vs EMA200.

Execution: signal at bar close, fill at next bar open, slippage by liquidity, commissions/fees, rolls before expiry. Sizing: contracts = risk per trade / (stop distance × point value), 0.5–1% risk; max portfolio risk, per-asset-class cap, daily loss limit, margin check.

Tests: in-sample with EMA 8/10/12/20/50/100 sensitivity · locked out-of-sample · rolling walk-forward · parameter heatmaps · cost stress (base / moderate / severe) · regimes (trend vs range, vol, bull/bear/sideways, market, asset class, year).

Metrics: total return, CAGR, max DD + duration, Sharpe, Sortino, Calmar, PF, win rate, avg win/loss, expectancy, trades, holding period, turnover, exposure-adjusted return, net of costs, by market / asset class / year, strategy correlations.

Deliverables: report, strategy spec, reproducible code, summary table, net equity curves, drawdowns + monthly tables, sensitivity, walk-forward, cost stress, recommendation, risk guide, disclaimer.
