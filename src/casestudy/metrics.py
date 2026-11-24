"""Performance metrics from an equity curve and a trade list."""
import numpy as np
import pandas as pd

TD = 252


def perf(equity, trades=None, exposure=None):
    eq = equity.dropna()
    r = eq.pct_change().dropna()
    years = max((eq.index[-1] - eq.index[0]).days / 365.25, 1e-9)
    total = eq.iloc[-1] / eq.iloc[0] - 1
    cagr = (eq.iloc[-1] / eq.iloc[0]) ** (1 / years) - 1 if eq.iloc[-1] > 0 else -1.0
    dd = eq / eq.cummax() - 1
    # longest time under water (calendar days)
    under = dd < 0
    dur, best, start = 0, 0, None
    for t, u in under.items():
        if u and start is None:
            start = t
        if not u and start is not None:
            best = max(best, (t - start).days); start = None
    if start is not None:
        best = max(best, (eq.index[-1] - start).days)
    sd, dn = r.std(), r[r < 0].std()
    out = dict(total_return=total, cagr=cagr, max_dd=dd.min(), max_dd_days=best,
               sharpe=r.mean() / sd * np.sqrt(TD) if sd > 0 else np.nan,
               sortino=r.mean() / dn * np.sqrt(TD) if dn and dn > 0 else np.nan,
               calmar=cagr / abs(dd.min()) if dd.min() < 0 else np.nan, vol=sd * np.sqrt(TD))
    if trades is not None and len(trades):
        t = trades
        w, l = t.pnl[t.pnl > 0], t.pnl[t.pnl <= 0]
        out.update(trades=len(t), trades_per_year=len(t) / years, win_rate=(t.pnl > 0).mean(),
                   profit_factor=w.sum() / -l.sum() if l.sum() < 0 else np.nan,
                   avg_win=w.mean() if len(w) else 0.0, avg_loss=l.mean() if len(l) else 0.0,
                   expectancy=t.pnl.mean(), expectancy_R=t.R.mean(), avg_hold_days=t.bars.mean())
    else:
        out.update(trades=0, trades_per_year=0, win_rate=np.nan, profit_factor=np.nan, avg_win=np.nan, avg_loss=np.nan,
                   expectancy=np.nan, expectancy_R=np.nan, avg_hold_days=np.nan)
    if exposure is not None:
        out["exposure"] = exposure
        out["exposure_adj_return"] = cagr / exposure if exposure > 0 else np.nan
    return out


def exposure_from_trades(trades, index):
    """Share of days with at least one open position."""
    if trades is None or not len(trades):
        return 0.0
    on = pd.Series(False, index=index)
    for a, b in zip(trades.entry_date, trades.exit_date):
        on.loc[a:b] = True
    return float(on.mean())


def monthly_table(equity):
    m = equity.resample("ME").last().pct_change().dropna()
    t = pd.DataFrame({"year": m.index.year, "month": m.index.month, "ret": m.values})
    return t.pivot(index="year", columns="month", values="ret")
