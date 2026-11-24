"""Load daily front-month series and turn them into a roll-adjusted (additive, "Panama") continuous series.

Yahoo `=F` series switch contracts on roll days, which shows up as an artificial overnight gap
(open_t - close_{t-1}). A roll is the largest |gap| / median absolute daily move (60 days) inside each calendar roll window, if > ROLL_Z. The gap is then removed from all EARLIER prices, so P&L in
points stays correct across rolls. Real news gaps of that size are rare; removing one costs (or
gives) one day's gap to every strategy equally. The number of detected rolls per year is reported
as a sanity check (≈4/yr for quarterly contracts, ≈12/yr for CL/NG).
"""
import numpy as np
import pandas as pd

ROLL_Z = 2.5


def load_raw(path):
    d = pd.read_csv(path, index_col=0, parse_dates=True).sort_index()
    d = d[~d.index.duplicated()]
    d = d[(d.high >= d.low) & d[["open", "high", "low", "close"]].notna().all(axis=1)]
    # bad ticks: an ISOLATED spike that reverts the next day (> 25% away, then > 20% back) is a data error,
    # e.g. Yahoo 6J 2001-12-17 printed 0.000783 instead of ~0.0078. Real crashes that stay down are kept
    # (e.g. silver -31% on 2026-01-30). Cleaning only, never used for signals.
    c = d.close
    up, back = c / c.shift(1) - 1, c.shift(-1) / c - 1
    bad = (up.abs() > 0.25) & (back.abs() > 0.20) & (np.sign(up) != np.sign(back))
    d = d[~bad.fillna(False)]
    # repair opens/high/low outside the bar (data errors): clamp into [low, high]
    d["high"] = d[["open", "high", "low", "close"]].max(axis=1)
    d["low"] = d[["open", "high", "low", "close"]].min(axis=1)
    return d[["open", "high", "low", "close"]].astype(float)


# Roll days. Yahoo `=F` switches to the next contract at expiry (checked by hand on ES/ZN 2024–2025).
#  - Equity index (ES NQ YM): first trading day after the 3rd Friday of Mar/Jun/Sep/Dec.
#  - FX (6E 6J 6B): first trading day after the Monday before the 3rd Wednesday of Mar/Jun/Sep/Dec.
#  - Treasuries (ZB ZN): first trading day after the 7th business day before the month's last business day (Mar/Jun/Sep/Dec).
#  - CL, NG, GC, SI, HG (approximate): inside a monthly window, the day with the largest |gap| / median |daily move|,
#    only if that ratio > ROLL_Z. Documented as an approximation in docs/DATA.md.
QUARTERLY = (3, 6, 9, 12)
WINDOWS = {"CL": range(14, 29), "NG": range(20, 32), "GC": range(20, 32), "SI": range(20, 32), "HG": range(20, 32)}


def _nth_weekday(y, m, weekday, n):
    d = pd.Timestamp(y, m, 1)
    d += pd.Timedelta(days=(weekday - d.weekday()) % 7)
    return d + pd.Timedelta(weeks=n - 1)


def _expiry(sym, y, m):
    if sym in ("ES", "NQ", "YM"):
        return _nth_weekday(y, m, 4, 3)                                   # 3rd Friday
    if sym in ("6E", "6J", "6B"):
        return _nth_weekday(y, m, 2, 3) - pd.Timedelta(days=2)            # Monday before 3rd Wednesday
    if sym in ("ZB", "ZN"):
        last = pd.Timestamp(y, m, 1) + pd.offsets.BMonthEnd(0)
        return last - pd.offsets.BDay(7)
    return None


def roll_adjust(d, sym=None, z=ROLL_Z):
    gap = d.open - d.close.shift(1)
    is_roll = pd.Series(False, index=d.index)
    if sym in ("ES", "NQ", "YM", "6E", "6J", "6B", "ZB", "ZN"):
        for y in range(d.index[0].year, d.index[-1].year + 1):
            for m in QUARTERLY:
                after = d.index[d.index > _expiry(sym, y, m)]
                if len(after) and after[0] > d.index[0]:
                    is_roll.loc[after[0]] = True
    elif sym in WINDOWS:
        scale = d.close.diff().abs().rolling(60, min_periods=20).median().shift(1)
        ratio = (gap.abs() / scale).fillna(0.0)
        cand = ratio[[t.day in WINDOWS[sym] for t in d.index]]
        for _, grp in cand.groupby([cand.index.year, cand.index.month]):
            if len(grp) and grp.max() > z:
                is_roll.loc[grp.idxmax()] = True
    adj = gap.where(is_roll, 0.0).fillna(0.0)
    back = adj[::-1].cumsum()[::-1].shift(-1).fillna(0.0)  # subtract each roll gap from every EARLIER price
    out = d.copy()
    for c in ["open", "high", "low", "close"]:
        out[c] = d[c] + back
    out["roll"] = is_roll
    return out


def load(path, sym=None):
    return roll_adjust(load_raw(path), sym)
