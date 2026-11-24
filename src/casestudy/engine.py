"""Daily portfolio backtest engine.

Timing (identical for every strategy):
  close of bar t : signals computed from bars <= t; trailing stops updated; orders queued.
  open of bar t+1: (1) a stop already beyond the open exits at the open (gap), (2) queued exits, (3) queued entries,
                   sized on equity at the close of t.
  during bar t+1 : stop hit -> exit at the stop level (no same-bar profit targets are assumed).
Costs per contract per side: commission + slippage (slip_ticks x tick x point_value x cost_mult).
Holding a position through a roll day costs one extra round turn.
Risk controls: risk per trade (% equity), max open risk for the portfolio and per asset class, margin cap,
daily loss limit (no new entries the next day), max contracts implied by margin.
"""
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from .specs import COMMISSION, spec


@dataclass
class Config:
    equity0: float = 1_000_000.0
    risk_per_trade: float = 0.005      # 0.5% of equity
    max_open_risk: float = 0.10        # portfolio
    max_class_risk: float = 0.04       # per asset class
    max_margin: float = 0.50           # of equity
    daily_loss_limit: float = 0.02     # stop new entries next day
    cost_mult: float = 1.0             # 1 base, 2 moderate, 3 severe
    allow_short: bool = True
    fractional: bool = False         # True = fractional contracts (measures the signal, not account granularity)


def run(data, signals, cfg=Config(), start=None, end=None):
    """data/signals: dict sym -> DataFrame (same index per sym). Returns (equity Series, trades DataFrame)."""
    syms = list(data)
    idx = sorted(set().union(*[data[s].index for s in syms]))
    idx = pd.DatetimeIndex(idx)
    if start is not None:
        idx = idx[idx >= pd.Timestamp(start)]
    if end is not None:
        idx = idx[idx <= pd.Timestamp(end)]
    A = {}
    for s in syms:
        d = data[s].reindex(idx)
        g = signals[s].reindex(idx)
        sp = spec(s)
        A[s] = dict(o=d.open.values, h=d.high.values, l=d.low.values, c=d.close.values,
                    roll=d.get("roll", pd.Series(False, index=idx)).fillna(False).values.astype(bool),
                    le=g.long_entry.fillna(False).values.astype(bool), se=g.short_entry.fillna(False).values.astype(bool),
                    lx=g.long_exit.fillna(False).values.astype(bool), sx=g.short_exit.fillna(False).values.astype(bool),
                    sll=g.sl_long.values, sls=g.sl_short.values, tl=g.trail_long.values, ts=g.trail_short.values,
                    atr=g.atr.values, **sp, side_cost=COMMISSION + sp["slip_ticks"] * sp["tick"] * sp["point_value"] * cfg.cost_mult)
    eq = cfg.equity0
    pos = {s: None for s in syms}          # dict(side, qty, entry, stop, risk, i0)
    pending = {s: None for s in syms}      # ('enter', side, stop_level) / ('exit',) / ('reverse', side, stop_level)
    trades, curve = [], np.empty(len(idx))
    skipped = []                          # entries the 0.5% risk rule could not size (qty rounded to 0)
    last_close = {s: np.nan for s in syms}
    block_entries = False
    for i in range(len(idx)):
        day_start_eq = eq
        for s in syms:
            a = A[s]; o, h, l, c = a["o"][i], a["h"][i], a["l"][i], a["c"][i]
            if np.isnan(o):
                pending[s] = None if pending[s] and pending[s][0] != "exit" else pending[s]
                continue
            p = pos[s]
            # mark the overnight move of an open position (from last close to today's open)
            if p is not None:
                eq += p["side"] * (o - last_close[s]) * p["qty"] * a["point_value"]
                if a["roll"][i]:
                    eq -= 2 * a["side_cost"] * p["qty"]
                # (1) gap through the stop
                if (p["side"] == 1 and o <= p["stop"]) or (p["side"] == -1 and o >= p["stop"]):
                    eq -= a["side_cost"] * p["qty"]
                    trades.append(_close(s, p, idx, i, o, a)); pos[s] = p = None
            # (2) queued exits / reversals
            q = pending[s]; pending[s] = None
            if q is not None and p is not None and q[0] in ("exit", "reverse"):
                eq -= a["side_cost"] * p["qty"]
                trades.append(_close(s, p, idx, i, o, a)); pos[s] = p = None
            # (3) queued entries
            if q is not None and q[0] in ("enter", "reverse") and p is None and not block_entries:
                side, lvl = q[1], q[2]
                dist = (o - lvl) * side
                prev_atr = a["atr"][i - 1] if i > 0 and np.isfinite(a["atr"][i - 1]) else np.nan
                if not np.isfinite(dist) or dist <= 0:
                    dist = prev_atr
                elif np.isfinite(prev_atr):
                    dist = max(dist, 0.5 * prev_atr)   # minimum stop = 0.5 ATR (a gap next to the stop must not inflate size)
                if np.isfinite(dist) and dist > 0:
                    qty = _size(s, dist, eq, a, pos, A, cfg)
                    if qty <= 0 and not cfg.fractional and cfg.risk_per_trade * eq < dist * a["point_value"]:
                        skipped.append((s, idx[i]))
                    if qty > 0:
                        eq -= a["side_cost"] * qty
                        pos[s] = p = dict(side=side, qty=qty, entry=o, stop=o - side * dist, risk=dist * qty * a["point_value"],
                                          i0=i, cls=a["asset_class"])
            # (4) intrabar stop
            if p is not None and ((p["side"] == 1 and l <= p["stop"]) or (p["side"] == -1 and h >= p["stop"])):
                px = p["stop"]
                eq += p["side"] * (px - o) * p["qty"] * a["point_value"] - a["side_cost"] * p["qty"]
                trades.append(_close(s, p, idx, i, px, a, marked_from=o)); pos[s] = p = None
            # mark open-to-close
            elif p is not None:
                eq += p["side"] * (c - o) * p["qty"] * a["point_value"]
                # trailing stop, ratchet only
                t = a["tl"][i] if p["side"] == 1 else a["ts"][i]
                if np.isfinite(t):
                    p["stop"] = max(p["stop"], t) if p["side"] == 1 else min(p["stop"], t)
            last_close[s] = c
            # queue tomorrow's orders from today's close
            le, se = a["le"][i], a["se"][i] and cfg.allow_short
            if p is None:
                if le: pending[s] = ("enter", 1, a["sll"][i])
                elif se: pending[s] = ("enter", -1, a["sls"][i])
            elif p["side"] == 1:
                if se: pending[s] = ("reverse", -1, a["sls"][i])
                elif a["lx"][i]: pending[s] = ("exit",)
            else:
                if le: pending[s] = ("reverse", 1, a["sll"][i])
                elif a["sx"][i]: pending[s] = ("exit",)
        block_entries = (eq - day_start_eq) < -cfg.daily_loss_limit * day_start_eq
        curve[i] = eq
    for s in syms:  # close anything still open at the last price, for the trade list only
        if pos[s] is not None:
            trades.append(_close(s, pos[s], idx, len(idx) - 1, last_close[s], A[s], final=True))
    T = pd.DataFrame(trades)
    T.attrs["skipped"] = skipped
    return pd.Series(curve, index=idx, name="equity"), T


def _size(s, dist, eq, a, pos, A, cfg):
    risk_cash = cfg.risk_per_trade * eq
    unit = dist * a["point_value"]
    rnd = (lambda x: x) if cfg.fractional else (lambda x: float(int(x)))
    qty = rnd(risk_cash / unit)
    if qty <= 0:
        return 0
    open_risk = sum(p["risk"] for p in pos.values() if p)
    cls_risk = sum(p["risk"] for p in pos.values() if p and p["cls"] == a["asset_class"])
    margin = sum(A[k]["margin"] * p["qty"] for k, p in pos.items() if p)
    room = min(cfg.max_open_risk * eq - open_risk, cfg.max_class_risk * eq - cls_risk)
    qty = min(qty, rnd(max(room, 0) / unit))
    qty = min(qty, rnd(max(cfg.max_margin * eq - margin, 0) / a["margin"]))
    return max(qty, 0)


def _close(s, p, idx, i, px, a, marked_from=None, final=False):
    pnl = p["side"] * (px - p["entry"]) * p["qty"] * a["point_value"] - 2 * a["side_cost"] * p["qty"]
    return dict(sym=s, cls=p["cls"], side=p["side"], entry_date=idx[p["i0"]], exit_date=idx[i], entry=p["entry"], exit=px,
                qty=p["qty"], pnl=pnl, R=pnl / p["risk"] if p["risk"] else np.nan, bars=i - p["i0"], open_at_end=final)
