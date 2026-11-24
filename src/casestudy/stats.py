"""Small, tested statistics helpers used by every result table."""
import numpy as np


def summary(r):
    """Trades, win rate, average R, t-stat and max drawdown (in R) of a series of trade results."""
    r = np.asarray(r, dtype=float)
    n = len(r)
    if n == 0:
        return dict(trades=0, win_rate=np.nan, avg_r=np.nan, t=np.nan, max_dd=np.nan)
    eq = np.cumsum(r)
    dd = (eq - np.maximum.accumulate(np.r_[0.0, eq][1:])).min()
    sd = r.std(ddof=1) if n > 1 else np.nan
    return dict(trades=n, win_rate=float((r > 0).mean()), avg_r=float(r.mean()),
                t=float(r.mean() / sd * np.sqrt(n)) if sd and sd > 0 else np.nan, max_dd=float(min(dd, 0.0)))
