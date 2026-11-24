"""Run the full study and write results/*.csv + results/figures/*.png. Then scripts/make_report.py writes REPORT.md.

    python scripts/run_all.py
"""
import glob
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from casestudy.engine import Config, run                      # noqa: E402
from casestudy.indicators import atr, ema                     # noqa: E402
from casestudy.intraday import run_orb                        # noqa: E402
from casestudy.metrics import exposure_from_trades, monthly_table, perf  # noqa: E402
from casestudy.prep import load                               # noqa: E402
from casestudy.specs import SPECS                             # noqa: E402
from casestudy.strategies import STRATEGIES                   # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
RES = os.path.join(ROOT, "results")
PERIODS = [8, 10, 12, 20, 50, 100]
SPLITS = {"in_sample": ("2001-01-01", "2015-12-31"), "validation": ("2016-01-01", "2020-12-31"), "test": ("2021-01-01", "2026-12-31")}
COSTS = {"base": 1.0, "moderate": 2.0, "severe": 3.0}
MAIN_COST = "moderate"   # pre-registered: pass criteria are judged net of moderate costs


def slice_perf(eq, T, a, b):
    e = eq.loc[a:b]
    t = T[(T.entry_date >= a) & (T.entry_date <= b)] if len(T) else T
    return perf(e / e.iloc[0] * 1e6, t, exposure_from_trades(t, e.index))


def main():
    # last complete daily bar = 2026-11-23 (the 24 Nov bar was still trading when the data was downloaded)
    data = {s: load(os.path.join(ROOT, "data/raw/daily", f"{s}.csv"), s).loc[:"2026-11-23"] for s in SPECS}
    rows, sens, curves, trades_main, cost_rows = [], [], {}, {}, []
    daily_rets = {}
    for name, f in STRATEGIES.items():
        for n in PERIODS:
            sig = {s: f(d, n) for s, d in data.items()}
            costs = COSTS if n == 12 else {MAIN_COST: COSTS[MAIN_COST]}
            for cname, cm in costs.items():
                eq, T = run(data, sig, Config(cost_mult=cm))
                if cname == MAIN_COST:
                    daily_rets[(name, n)] = eq.pct_change().fillna(0.0)
                    p = perf(eq, T)
                    sens.append(dict(strategy=name, ema=n, **{k: p[k] for k in ("sharpe", "cagr", "max_dd", "profit_factor", "trades")},
                                     sharpe_in_sample=slice_perf(eq, T, *SPLITS["in_sample"])["sharpe"]))
                if n == 12:
                    p = perf(eq, T, exposure_from_trades(T, eq.index))
                    cost_rows.append(dict(strategy=name, cost=cname, **p))
                    if cname == MAIN_COST:
                        curves[name] = eq; trades_main[name] = T
                        for sp, (a, b) in SPLITS.items():
                            rows.append(dict(strategy=name, split=sp, **slice_perf(eq, T, a, b)))
            print(name, n, flush=True)
    pd.DataFrame(rows).to_csv(f"{RES}/splits_moderate.csv", index=False)
    pd.DataFrame(sens).to_csv(f"{RES}/ema_sensitivity.csv", index=False)
    pd.DataFrame(cost_rows).to_csv(f"{RES}/cost_stress.csv", index=False)
    pd.DataFrame(curves).to_csv(f"{RES}/equity_moderate.csv")
    allT = pd.concat([t.assign(strategy=k) for k, t in trades_main.items()], ignore_index=True)
    allT.to_csv(f"{RES}/trades_moderate.csv", index=False)

    # ---- walk-forward: choose the EMA period with the best Sharpe on the previous 5 years, apply it to the next year
    wf_rows, wf_curves = [], {}
    for name in STRATEGIES:
        oos = []
        for y in range(2006, 2027):
            tr_a, tr_b = f"{y-5}-01-01", f"{y-1}-12-31"
            best = max(PERIODS, key=lambda n: _sharpe(daily_rets[(name, n)].loc[tr_a:tr_b]))
            r = daily_rets[(name, best)].loc[f"{y}-01-01":f"{y}-12-31"]
            oos.append(r); wf_rows.append(dict(strategy=name, year=y, chosen_ema=best, ret=(1 + r).prod() - 1))
        r = pd.concat(oos)
        wf_curves[name] = (1 + r).cumprod() * 1e6
    pd.DataFrame(wf_rows).to_csv(f"{RES}/walk_forward_years.csv", index=False)
    wfc = pd.DataFrame(wf_curves); wfc.to_csv(f"{RES}/walk_forward_equity.csv")
    pd.DataFrame([dict(strategy=k, **perf(wfc[k].dropna())) for k in wfc]).to_csv(f"{RES}/walk_forward_summary.csv", index=False)

    # ---- breakdowns of the EMA-12 moderate-cost trades
    regimes = _regimes(data)
    allT["year"] = pd.to_datetime(allT.exit_date).dt.year
    allT = allT.merge(regimes, how="left", left_on=["sym", "entry_date"], right_index=True)
    for col in ["sym", "cls", "year", "trend", "vol", "market"]:
        g = allT.groupby(["strategy", col]).agg(trades=("pnl", "size"), pnl=("pnl", "sum"), avg_R=("R", "mean"), win=("pnl", lambda x: (x > 0).mean()))
        g.reset_index().to_csv(f"{RES}/by_{col}.csv", index=False)
    rets = pd.DataFrame({k: v.pct_change() for k, v in curves.items()})
    rets.corr().to_csv(f"{RES}/correlations.csv")
    for k, v in curves.items():
        monthly_table(v).to_csv(f"{RES}/monthly/{k.split()[0]}.csv")

    # ---- Strategy 11, intraday
    files = sorted(glob.glob(os.path.join(ROOT, "data/raw/intraday/nq_duka_m1_*.parquet")))
    m1 = pd.concat([pd.read_parquet(f) for f in files]).sort_index()
    m1 = m1[~m1.index.duplicated()][["o", "h", "l", "c"]] / 1000.0
    m1.index = m1.index.tz_convert("America/New_York")
    s11 = []
    for cname, cm in COSTS.items():
        for n in PERIODS:
            if cname != MAIN_COST and n != 12:
                continue
            t = run_orb(m1, "NQ", n=n, cost_mult=cm)
            t.assign(cost=cname, ema=n).to_csv(f"{RES}/s11_trades_{cname}_ema{n}.csv", index=False)
            for sp, (a, b) in {"in_sample": ("2022-11-01", "2024-10-31"), "test": ("2024-11-01", "2026-12-31"), "all": ("2000", "2100")}.items():
                u = t[(t.date >= a) & (t.date <= b)]
                s11.append(dict(cost=cname, ema=n, split=sp, trades=len(u), days=m1.loc[a:b].index.normalize().nunique(),
                                win_rate=(u.R > 0).mean(), avg_R=u.R.mean(), t=u.R.mean() / u.R.std() * np.sqrt(len(u)) if len(u) > 1 else np.nan,
                                pnl=u.pnl.sum(), profit_factor=u.pnl[u.pnl > 0].sum() / -u.pnl[u.pnl < 0].sum() if (u.pnl < 0).any() else np.nan))
    pd.DataFrame(s11).to_csv(f"{RES}/s11_summary.csv", index=False)
    json.dump(dict(data_days={s: [str(d.index[0].date()), str(d.index[-1].date()), int(len(d)), int(d.roll.sum())] for s, d in data.items()},
                   intraday_days=int(m1.index.normalize().nunique())), open(f"{RES}/data_summary.json", "w"), indent=1)
    print("done")


def _sharpe(r):
    r = r.dropna()
    return r.mean() / r.std() * np.sqrt(252) if len(r) > 20 and r.std() > 0 else -9


def _regimes(data):
    out = []
    for s, d in data.items():
        e50, e200, a = ema(d.close, 50), ema(d.close, 200), atr(d, 14)
        trend_strength = (e50 - e50.shift(20)).abs() / a
        atrp = a / d.close.abs()
        slope200 = e200 - e200.shift(20)
        f = pd.DataFrame(index=d.index)
        f["trend"] = np.where(trend_strength > trend_strength.rolling(252, min_periods=60).median(), "trending", "non-trending")
        f["vol"] = np.where(atrp > atrp.rolling(252, min_periods=60).median(), "high-vol", "low-vol")
        f["market"] = np.select([(d.close > e200) & (slope200 > 0), (d.close < e200) & (slope200 < 0)], ["bull", "bear"], "sideways")
        f["sym"] = s
        out.append(f.reset_index().rename(columns={"index": "entry_date", "Date": "entry_date"}))
    r = pd.concat(out)
    r = r.rename(columns={r.columns[0]: "entry_date"})
    return r.set_index(["sym", "entry_date"])


if __name__ == "__main__":
    os.makedirs(f"{RES}/monthly", exist_ok=True)
    os.makedirs(f"{RES}/figures", exist_ok=True)
    main()
