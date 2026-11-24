# Data notes

## Daily futures (primary study)
- **Source:** Yahoo Finance chart API, front-month continuous `=F` series (`src/casestudy/data.py::yahoo_daily`). Downloaded 24 Nov 2026; the last complete bar used is **2026-11-23**. Raw CSVs live in `data/raw/daily/` and are not committed (rebuild with the loader).
- **Not exchange-grade:** no open interest; the volume is the front month's; settlement vs last-trade conventions are Yahoo's.
- **Cleaning (`prep.load_raw`):** duplicate dates dropped; high/low widened to contain open/close; isolated spike-and-revert bars (> 25% away, then > 20% back the next day) removed. Removed bars: CL 2020-04-21, NG 2022-01-27, GC 2009-11-23, 6J 2001-12-17 (printed 0.000783 instead of ~0.0078). Real crashes are kept (silver −31% on 2026-01-30, gold −11% the same day).
- **Roll adjustment (`prep.roll_adjust`):** Yahoo switches to the next contract at expiry, which creates an artificial overnight gap. The gap on each roll day is subtracted from every earlier price (additive "Panama" back-adjustment), so P&L in points is preserved; early prices can be negative (HG, CL), which is harmless for point-based P&L and EMAs.
  - ES, NQ, YM: first trading day after the 3rd Friday of Mar/Jun/Sep/Dec (verified by hand: 2024-03-18, 2025-09-22, 2025-12-22).
  - 6E, 6J, 6B: first trading day after the Monday before the 3rd Wednesday of Mar/Jun/Sep/Dec.
  - ZB, ZN: first trading day after the 7th business day before the last business day of Mar/Jun/Sep/Dec.
  - CL, NG, GC, SI, HG (approximate): inside a monthly window, the day with the largest |gap| / 60-day median |daily move|, if > 2.5.
  - Rolls detected over 26 years: ES 104, NQ 104, YM 98, CL 34, NG 72, GC 70, SI 128, HG 69, 6E 105, 6J 105, 6B 104, ZB 104, ZN 104. CL and NG are under-detected (monthly contracts with small spreads look like normal days); their residual roll gaps add noise in both directions.
- **Costs of rolling:** a position held through a roll day pays one extra round turn.
- **Contract specs (`specs.py`):** standard CME point values and ticks; margins are approximate 2026 levels applied to the whole history (only used for the margin cap).

## Intraday (Strategy 11)
- Dukascopy 1-minute BID candles of the Nasdaq-100 CFD (`USATECHIDXUSD`), UTC → New York time, resampled to 5-minute bars in 09:30–16:00.
- A CFD proxy for NQ: same underlying index, no futures basis or roll; spread assumed ≈ 1 NQ tick inside the cost model.
- Coverage: 566 sessions between Nov 2022 and Nov 2026 (the free feed throttles; missing days are random, not selected).
