"""Strategy 11 (intraday): 30-minute opening-range breakout with a 12-EMA filter, on 5-minute bars.

Regular session 09:30–16:00 New York. Opening range = 09:30–10:00 high/low.
Signal at the close of a 5-min bar (10:00 or later): close > OR high AND close > EMA12(5-min) -> long; mirror short.
Fill at the next 5-min bar open. Initial stop: fixed distance = the opening-range height (from the entry).
Trailing stop: 2 x ATR14 (5-min), ratcheting. Exit at the 15:55 bar close at the latest. One trade per day.
Costs per side: commission + 1 tick slippage x cost_mult. Results in R (1R = initial stop distance) and in USD
for 0.5% risk per trade on $1M (contracts rounded down).
Data: Dukascopy 1-min CFD (Nasdaq-100 USATECHIDXUSD), a proxy for NQ futures; disclosed in the report.
"""
import numpy as np
import pandas as pd

from .indicators import atr, ema
from .specs import COMMISSION, spec


def bars5(m1):
    rth = m1.between_time("09:30", "15:59")
    return rth.resample("5min", label="left", closed="left").agg({"o": "first", "h": "max", "l": "min", "c": "last"}).dropna()


def run_orb(m1, sym="NQ", n=12, cost_mult=1.0, equity=1_000_000.0, risk=0.005):
    sp = spec(sym)
    side_cost_pts = (COMMISSION / sp["point_value"]) + sp["slip_ticks"] * sp["tick"] * cost_mult
    b = bars5(m1)
    d = b.rename(columns={"o": "open", "h": "high", "l": "low", "c": "close"})
    d["ema"] = ema(d.close, n)          # continuous across days (uses only past bars)
    d["atr"] = atr(d, 14)
    out = []
    for day, g in d.groupby(d.index.date):
        orr = g.between_time("09:30", "09:55")
        if len(orr) < 6:
            continue
        hi, lo = orr.high.max(), orr.low.min(); rng = hi - lo
        if rng <= 0:
            continue
        rest = g.between_time("10:00", "15:55")
        times = list(rest.index)
        for k in range(len(times) - 1):
            r = rest.iloc[k]
            side = 1 if (r.close > hi and r.close > r.ema) else (-1 if (r.close < lo and r.close < r.ema) else 0)
            if side == 0:
                continue
            nxt = rest.iloc[k + 1]
            entry = nxt.open
            stop = entry - side * rng
            exit_px = None
            for j in range(k + 1, len(times)):
                bar = rest.iloc[j]
                if (side == 1 and bar.low <= stop) or (side == -1 and bar.high >= stop):
                    exit_px = min(stop, bar.open) if side == 1 else max(stop, bar.open)
                    break
                trail = bar.close - side * 2 * bar.atr
                stop = max(stop, trail) if side == 1 else min(stop, trail)
            if exit_px is None:
                exit_px = rest.iloc[-1].close
            pts = side * (exit_px - entry) - 2 * side_cost_pts
            qty = int(equity * risk // (rng * sp["point_value"]))
            out.append(dict(date=pd.Timestamp(day), side=side, entry=entry, exit=exit_px, R=pts / rng, qty=qty,
                            pnl=pts * qty * sp["point_value"]))
            break
    return pd.DataFrame(out)
