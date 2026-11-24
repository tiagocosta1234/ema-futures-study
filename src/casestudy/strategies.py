"""The 11 daily strategies (Strategy 11 is intraday, see intraday.py).

Each function takes a daily OHLC frame and the fast EMA period `n` (12 = the study default) and returns
a frame of signals evaluated at the CLOSE of bar t, to be executed by the engine at the OPEN of bar t+1:
  long_entry, short_entry, long_exit, short_exit : bool
  sl_long, sl_short   : initial stop LEVEL for a new long/short (price)
  trail_long, trail_short : trailing-stop candidate level (NaN = no trailing); the engine only ratchets stops
                            in the trade's favour.
Slower EMAs scale with n (26/12·n, 50/12·n) so that the parameter sweep moves the whole system, except where the
brief fixes them (50 in S4/S5, 200 in S10/S12).
"""
import numpy as np
import pandas as pd

from .indicators import atr, cross_down, cross_up, ema


def _base(d, n):
    e = ema(d.close, n)
    a = atr(d, 14)
    s = pd.DataFrame(index=d.index)
    for c in ["long_entry", "short_entry", "long_exit", "short_exit"]:
        s[c] = False
    s["sl_long"] = d.close - 2 * a
    s["sl_short"] = d.close + 2 * a
    s["trail_long"] = np.nan
    s["trail_short"] = np.nan
    s["atr"] = a
    return s, e, a


def _fresh(x):
    return x & ~x.shift(1, fill_value=False)


def s01_price_cross(d, n=12):
    s, e, a = _base(d, n)
    s["long_entry"] = cross_up(d.close, e)
    s["short_entry"] = cross_down(d.close, e)
    s["long_exit"], s["short_exit"] = s.short_entry, s.long_entry
    return s


def s02_slope(d, n=12, lb=5):
    s, e, a = _base(d, n)
    slope = e - e.shift(lb)
    L = (d.close > e) & (slope > 0)
    S = (d.close < e) & (slope < 0)
    s["long_entry"], s["short_entry"] = _fresh(L), _fresh(S)
    s["long_exit"] = (d.close < e) | (slope <= 0)
    s["short_exit"] = (d.close > e) | (slope >= 0)
    return s


def s03_donchian(d, n=12, look=20, trail=10):
    s, e, a = _base(d, n)
    hh = d.high.rolling(look).max().shift(1)
    ll = d.low.rolling(look).min().shift(1)
    s["long_entry"] = (d.close > hh) & (d.close > e)
    s["short_entry"] = (d.close < ll) & (d.close < e)
    s["trail_long"] = d.low.rolling(trail).min()
    s["trail_short"] = d.high.rolling(trail).max()
    return s


def s04_pullback(d, n=12, swing=5):
    s, e, a = _base(d, n)
    slow = ema(d.close, 50 if n < 50 else 200)
    up, dn = e > slow, e < slow
    s["long_entry"] = up & (d.low <= e) & (d.close > e)
    s["short_entry"] = dn & (d.high >= e) & (d.close < e)
    s["sl_long"] = d.low.rolling(swing).min()
    s["sl_short"] = d.high.rolling(swing).max()
    s["long_exit"], s["short_exit"] = ~up, ~dn
    return s


def s05_ema_cross(d, n=12):
    s, e, a = _base(d, n)
    slow = ema(d.close, 50 if n < 50 else 200)
    s["long_entry"], s["short_entry"] = cross_up(e, slow), cross_down(e, slow)
    s["long_exit"], s["short_exit"] = s.short_entry, s.long_entry
    s["sl_long"], s["sl_short"] = d.close - 3 * a, d.close + 3 * a
    return s


def s06_triple(d, n=12):
    s, e, a = _base(d, n)
    m, sl = ema(d.close, round(26 / 12 * n)), ema(d.close, round(50 / 12 * n))
    s["long_entry"] = _fresh((e > m) & (m > sl))
    s["short_entry"] = _fresh((e < m) & (m < sl))
    s["long_exit"], s["short_exit"] = cross_down(e, m), cross_up(e, m)
    s["sl_long"], s["sl_short"] = d.close - 3 * a, d.close + 3 * a
    return s


def s07_macd(d, n=12):
    s, e, a = _base(d, n)
    macd = e - ema(d.close, round(26 / 12 * n))
    sig = macd.ewm(span=9, adjust=False).mean()
    s["long_entry"] = cross_up(macd, sig) & (d.close > e)
    s["short_entry"] = cross_down(macd, sig) & (d.close < e)
    s["long_exit"], s["short_exit"] = cross_down(macd, sig), cross_up(macd, sig)
    return s


def s08_atr_trend(d, n=12):
    s, e, a = _base(d, n)
    rising = a > a.shift(5)
    s["long_entry"] = _fresh((d.close > e) & rising)
    s["short_entry"] = _fresh((d.close < e) & rising)
    s["long_exit"], s["short_exit"] = d.close < e, d.close > e
    s["trail_long"], s["trail_short"] = d.close - 3 * a, d.close + 3 * a
    return s


def s09_vol_breakout(d, n=12, look=20):
    s, e, a = _base(d, n)
    hh = d.high.rolling(look).max().shift(1)
    ll = d.low.rolling(look).min().shift(1)
    s["long_entry"] = (d.close > hh) & (e > e.shift(1))
    s["short_entry"] = (d.close < ll) & (e < e.shift(1))
    s["long_exit"], s["short_exit"] = s.short_entry, s.long_entry
    s["trail_long"], s["trail_short"] = d.close - 2 * a, d.close + 2 * a
    return s


def s10_mean_reversion(d, n=12, k=2.0):
    s, e, a = _base(d, n)
    dev = d.close - e
    z = dev / dev.rolling(20).std()
    e50, e200 = ema(d.close, 50), ema(d.close, 200)
    strongly_bear = (e50 < e200) & (e50 < e50.shift(20))
    strongly_bull = (e50 > e200) & (e50 > e50.shift(20))
    s["long_entry"] = (z < -k) & ~strongly_bear
    s["short_entry"] = (z > k) & ~strongly_bull
    s["long_exit"], s["short_exit"] = d.close >= e, d.close <= e
    return s


def s12_regime(d, n=12):
    s, e, a = _base(d, n)
    reg = ema(d.close, 200)
    s["long_entry"] = cross_up(d.close, e) & (e > reg)
    s["short_entry"] = cross_down(d.close, e) & (e < reg)
    s["long_exit"], s["short_exit"] = cross_down(d.close, e), cross_up(d.close, e)
    return s


STRATEGIES = {
    "S01 Price/EMA cross": s01_price_cross, "S02 EMA slope": s02_slope, "S03 Donchian+EMA": s03_donchian,
    "S04 EMA pullback": s04_pullback, "S05 EMA12/50 cross": s05_ema_cross, "S06 Triple EMA": s06_triple,
    "S07 MACD+EMA": s07_macd, "S08 ATR trend": s08_atr_trend, "S09 Vol breakout": s09_vol_breakout,
    "S10 Mean reversion": s10_mean_reversion, "S12 Regime switch": s12_regime,
}
