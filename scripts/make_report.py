"""Build figures and results/summary tables from results/*.csv, and judge each strategy against the
pre-registered criteria in docs/PLAN.md. Writes results/verdicts.csv and results/report_tables.md
(REPORT.md quotes these tables)."""
import json
import os

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
RES, FIG = os.path.join(ROOT, "results"), os.path.join(ROOT, "results", "figures")
SURF, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
BLUE, ORANGE, AQUA, GOOD, CRIT = "#2a78d6", "#eb6834", "#1baf7a", "#0ca30c", "#d03b3b"
DIV = LinearSegmentedColormap.from_list("div", [CRIT, "#e4e3df", BLUE])
plt.rcParams.update({"text.parse_math": False, "font.size": 9, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "figure.facecolor": SURF, "axes.facecolor": SURF})


def fmt(x, pct=False, d=2):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "–"
    return f"{100*x:.1f}%" if pct else f"{x:.{d}f}"


def main():
    split = pd.read_csv(f"{RES}/splits_moderate.csv")
    sens = pd.read_csv(f"{RES}/ema_sensitivity.csv")
    cost = pd.read_csv(f"{RES}/cost_stress.csv")
    eq = pd.read_csv(f"{RES}/equity_moderate.csv", index_col=0, parse_dates=True)
    wf = pd.read_csv(f"{RES}/walk_forward_summary.csv")
    wfe = pd.read_csv(f"{RES}/walk_forward_equity.csv", index_col=0, parse_dates=True)
    bysym, bycls = pd.read_csv(f"{RES}/by_sym.csv"), pd.read_csv(f"{RES}/by_cls.csv")
    corr = pd.read_csv(f"{RES}/correlations.csv", index_col=0)
    s11 = pd.read_csv(f"{RES}/s11_summary.csv")
    names = list(eq.columns)
    T = pd.read_csv(f"{RES}/trades_moderate.csv")
    conc = {}
    for s_ in names:
        t = T[T.strategy == s_].pnl.sort_values(ascending=False)
        k = max(1, int(round(0.01 * len(t))))
        conc[s_] = (t.sum(), t.iloc[k:].sum(), k)

    # ---------- verdicts against the pre-registered criteria
    V = []
    for s in names:
        t = split[(split.strategy == s) & (split.split == "test")].iloc[0]
        full_mod = cost[(cost.strategy == s) & (cost.cost == "moderate")].iloc[0]
        sev = cost[(cost.strategy == s) & (cost.cost == "severe")].iloc[0]
        w = wf[wf.strategy == s].iloc[0]
        ms = bysym[bysym.strategy == s]; mc = bycls[bycls.strategy == s]
        se = sens[sens.strategy == s].set_index("ema").sharpe
        c = {
            "1 test Sharpe > 0.3": t.sharpe > 0.3,
            "2 walk-forward positive": w.total_return > 0,
            "3 test PF > 1.1 and >= 100 trades": (t.profit_factor > 1.1) and (t.trades >= 100),
            "4 >= 60% markets and >= 3/5 classes positive": ((ms.pnl > 0).mean() >= 0.6) and ((mc.pnl > 0).sum() >= 3),
            "5 EMA 10 & 20 keep >= 50% of EMA-12 Sharpe": (se.get(12, -1) > 0) and (se.get(10, -9) >= 0.5 * se[12]) and (se.get(20, -9) >= 0.5 * se[12]),
            "6 positive under severe costs": sev.total_return > 0,
        }
        passed = sum(c.values())
        V.append(dict(strategy=s, verdict="ROBUST" if passed == 6 else ("FRAGILE" if passed >= 3 else "REJECTED"), passed=passed,
                      failed="; ".join(k for k, v in c.items() if not v), full_sharpe=full_mod.sharpe, full_cagr=full_mod.cagr,
                      full_max_dd=full_mod.max_dd, test_sharpe=t.sharpe, test_cagr=t.cagr, test_trades=t.trades, wf_sharpe=w.sharpe,
                      severe_sharpe=sev.sharpe, pnl_total=conc[s][0], pnl_ex_top1pct=conc[s][1], top_n=conc[s][2], markets_pos=f"{(ms.pnl > 0).sum()}/{len(ms)}", classes_pos=f"{(mc.pnl > 0).sum()}/{len(mc)}"))
    V = pd.DataFrame(V).sort_values(["passed", "test_sharpe"], ascending=False)
    V.to_csv(f"{RES}/verdicts.csv", index=False)

    # ---------- figures
    fig, axs = plt.subplots(3, 4, figsize=(16, 10), sharex=True)
    for ax, s in zip(axs.flat, names):
        e = eq[s] / 1e6
        ax.plot(e.index, e, color=BLUE, lw=1.3)
        for a, b, lab in [("2016-01-01", "2020-12-31", "valid."), ("2021-01-01", "2026-12-31", "test")]:
            ax.axvspan(pd.Timestamp(a), pd.Timestamp(b), color=GRID, alpha=0.5 if lab == "test" else 0.25, lw=0)
        ax.axhline(1, color=INK2, lw=0.6)
        v = V.set_index("strategy").loc[s]
        ax.set_title(f"{s}\nSharpe {v.full_sharpe:.2f} · CAGR {100*v.full_cagr:.1f}% · {v.verdict}", loc="left", fontsize=9, color=INK)
        ax.grid(color=GRID, lw=0.6); ax.spines[["top", "right"]].set_visible(False)
    axs.flat[-1].axis("off")
    fig.suptitle("Equity (x initial), 13 futures, net of MODERATE costs, EMA 12 · light grey = validation 2016–20, darker = locked test 2021–26",
                 x=0.01, ha="left", fontsize=11, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.96)); fig.savefig(f"{FIG}/equity_curves.png", dpi=110); plt.close(fig)

    fig, axs = plt.subplots(3, 4, figsize=(16, 9), sharex=True, sharey=True)
    for ax, s in zip(axs.flat, names):
        e = eq[s]; dd = e / e.cummax() - 1
        ax.fill_between(dd.index, dd * 100, 0, color=CRIT, alpha=0.35, lw=0)
        ax.set_title(f"{s} · max {100*dd.min():.0f}%", loc="left", fontsize=9, color=INK)
        ax.grid(color=GRID, lw=0.6); ax.spines[["top", "right"]].set_visible(False)
    axs.flat[-1].axis("off")
    fig.suptitle("Drawdowns (%), moderate costs, EMA 12", x=0.01, ha="left", fontsize=11, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.96)); fig.savefig(f"{FIG}/drawdowns.png", dpi=110); plt.close(fig)

    H = sens.pivot(index="strategy", columns="ema", values="sharpe_in_sample").loc[names]
    fig, ax = plt.subplots(figsize=(8.5, 6.2))
    lim = max(0.6, np.nanmax(np.abs(H.values)))
    im = ax.imshow(H.values, cmap=DIV, vmin=-lim, vmax=lim, aspect="auto")
    for i in range(H.shape[0]):
        for j in range(H.shape[1]):
            ax.text(j, i, f"{H.values[i, j]:.2f}", ha="center", va="center", fontsize=8.5, color=INK)
    ax.set_xticks(range(H.shape[1])); ax.set_xticklabels([f"EMA {c}" for c in H.columns])
    ax.set_yticks(range(H.shape[0])); ax.set_yticklabels(H.index)
    ax.set_title("Parameter sensitivity: IN-SAMPLE (2001–15) Sharpe by fast-EMA period (moderate costs)", loc="left", fontsize=10.5, color=INK)
    fig.colorbar(im, ax=ax, shrink=0.8, label="Sharpe"); fig.tight_layout(); fig.savefig(f"{FIG}/ema_heatmap.png", dpi=120); plt.close(fig)

    fig, ax = plt.subplots(figsize=(12, 4.8))
    x = np.arange(len(names)); w = 0.26
    for k, (c, col) in enumerate([("base", BLUE), ("moderate", ORANGE), ("severe", AQUA)]):
        v = [cost[(cost.strategy == s) & (cost.cost == c)].sharpe.iloc[0] for s in names]
        ax.bar(x + (k - 1) * w, v, w - 0.03, color=col, label=c)
    ax.axhline(0, color=INK2, lw=0.8); ax.set_xticks(x); ax.set_xticklabels([s.split(" ", 1)[0] for s in names])
    ax.legend(frameon=False, title="costs"); ax.set_ylabel("Sharpe (full sample)")
    ax.set_title("Transaction-cost stress test (1x / 2x / 3x slippage)", loc="left", fontsize=10.5, color=INK)
    ax.grid(axis="y", color=GRID, lw=0.6); ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(f"{FIG}/cost_stress.png", dpi=120); plt.close(fig)

    fig, axs = plt.subplots(3, 4, figsize=(16, 9), sharex=True)
    for ax, s in zip(axs.flat, names):
        e = wfe[s].dropna() / 1e6
        ax.plot(e.index, e, color=ORANGE, lw=1.3); ax.axhline(1, color=INK2, lw=0.6)
        w_ = wf[wf.strategy == s].iloc[0]
        ax.set_title(f"{s}\nwalk-forward Sharpe {w_.sharpe:.2f} · CAGR {100*w_.cagr:.1f}%", loc="left", fontsize=9, color=INK)
        ax.grid(color=GRID, lw=0.6); ax.spines[["top", "right"]].set_visible(False)
    axs.flat[-1].axis("off")
    fig.suptitle("Walk-forward (2006–2026): EMA period re-chosen each year on the previous 5 years, applied to the next year only",
                 x=0.01, ha="left", fontsize=11, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.95)); fig.savefig(f"{FIG}/walk_forward.png", dpi=110); plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 6.5))
    im = ax.imshow(corr.loc[names, names].values, cmap=DIV, vmin=-1, vmax=1)
    short = [s.split(" ", 1)[0] for s in names]
    ax.set_xticks(range(len(names))); ax.set_xticklabels(short); ax.set_yticks(range(len(names))); ax.set_yticklabels(names)
    for i in range(len(names)):
        for j in range(len(names)):
            ax.text(j, i, f"{corr.loc[names[i], names[j]]:.2f}", ha="center", va="center", fontsize=7, color=INK)
    ax.set_title("Correlation of daily strategy returns (EMA 12, moderate costs)", loc="left", fontsize=10.5, color=INK)
    fig.colorbar(im, ax=ax, shrink=0.8); fig.tight_layout(); fig.savefig(f"{FIG}/correlations.png", dpi=120); plt.close(fig)

    P = bycls.pivot(index="strategy", columns="cls", values="pnl").loc[names] / 1e3
    fig, ax = plt.subplots(figsize=(8, 6))
    lim = np.nanmax(np.abs(P.values))
    im = ax.imshow(P.values, cmap=DIV, vmin=-lim, vmax=lim, aspect="auto")
    for i in range(P.shape[0]):
        for j in range(P.shape[1]):
            ax.text(j, i, f"{P.values[i, j]:,.0f}", ha="center", va="center", fontsize=8, color=INK)
    ax.set_xticks(range(P.shape[1])); ax.set_xticklabels(P.columns); ax.set_yticks(range(P.shape[0])); ax.set_yticklabels(P.index)
    ax.set_title("Net P&L by asset class, $ thousands (EMA 12, moderate costs, 2001–2026)", loc="left", fontsize=10.5, color=INK)
    fig.colorbar(im, ax=ax, shrink=0.8); fig.tight_layout(); fig.savefig(f"{FIG}/by_asset_class.png", dpi=120); plt.close(fig)

    t11 = pd.read_csv(f"{RES}/s11_trades_moderate_ema12.csv", parse_dates=["date"])
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(t11.date, t11.R.cumsum(), color=BLUE, lw=1.6); ax.axhline(0, color=INK2, lw=0.8)
    ax.axvline(pd.Timestamp("2024-11-01"), color=INK2, ls="--", lw=1); ax.text(pd.Timestamp("2024-11-10"), t11.R.cumsum().max(), "test", color=INK2)
    s = s11[(s11.cost == "moderate") & (s11.ema == 12) & (s11.split == "all")].iloc[0]
    ax.set_title(f"S11 opening-range breakout + EMA12, NQ 5-min (CFD proxy): cumulative R · {int(s.trades)} trades · avg {s.avg_R:+.3f}R",
                 loc="left", fontsize=10.5, color=INK)
    ax.grid(color=GRID, lw=0.6); ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(f"{FIG}/s11_intraday.png", dpi=120); plt.close(fig)

    # ---------- turnover and margin usage (from the trade list; back-adjusted prices -> |entry| approximates notional)
    import sys
    sys.path.insert(0, os.path.join(ROOT, "src"))
    from casestudy.specs import SPECS
    tm = []
    for s_ in names:
        t = T[T.strategy == s_].copy()
        e = eq[s_]
        pv = t.sym.map(lambda k: SPECS[k][1]); mg = t.sym.map(lambda k: SPECS[k][3])
        years = (e.index[-1] - e.index[0]).days / 365.25
        turnover = (2 * t.qty * t.entry.abs() * pv).sum() / e.mean() / years
        m = pd.Series(0.0, index=e.index)
        for a, b, q in zip(pd.to_datetime(t.entry_date), pd.to_datetime(t.exit_date), t.qty * mg):
            m.loc[a:b] += q
        tm.append(dict(strategy=s_, turnover_x_per_year=turnover, avg_margin_pct=(m / e).mean(), max_margin_pct=(m / e).max()))
    TM = pd.DataFrame(tm).set_index("strategy"); TM.to_csv(f"{RES}/turnover_margin.csv")
    IA = pd.read_csv(f"{RES}/integer_contracts_appendix.csv").set_index("strategy")

    # ---------- markdown tables for the report
    md = ["| Strategy | Verdict | Criteria met | Full Sharpe | Full CAGR | Max DD | Test Sharpe | Test CAGR | Test trades | Walk-fwd Sharpe | Severe-cost Sharpe | Markets + | Classes + | Net P&L $k | Without top 1% trades $k |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in V.iterrows():
        md.append(f"| {r.strategy} | **{r.verdict}** | {r.passed}/6 | {fmt(r.full_sharpe)} | {fmt(r.full_cagr, True)} | {fmt(r.full_max_dd, True)} | "
                  f"{fmt(r.test_sharpe)} | {fmt(r.test_cagr, True)} | {int(r.test_trades)} | {fmt(r.wf_sharpe)} | {fmt(r.severe_sharpe)} | {r.markets_pos} | {r.classes_pos} | {r.pnl_total/1e3:,.0f} | {r.pnl_ex_top1pct/1e3:,.0f} (−{r.top_n}) |")
    md += ["", "Failed criteria:", ""] + [f"- **{r.strategy}**: {r.failed or 'none'}" for _, r in V.iterrows()]
    full = cost[cost.cost == "moderate"].set_index("strategy").loc[names]
    md += ["", "| Strategy | Total return | CAGR | Max DD | DD days | Sharpe | Sortino | Calmar | PF | Win rate | Avg win $ | Avg loss $ | Expectancy $ | Exp. R | Trades/yr | Hold days | Exposure | Exp.-adj. return |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for s, r in full.iterrows():
        md.append(f"| {s} | {fmt(r.total_return, True)} | {fmt(r.cagr, True)} | {fmt(r.max_dd, True)} | {int(r.max_dd_days)} | {fmt(r.sharpe)} | {fmt(r.sortino)} | "
                  f"{fmt(r.calmar)} | {fmt(r.profit_factor)} | {fmt(r.win_rate, True)} | {r.avg_win:,.0f} | {r.avg_loss:,.0f} | {r.expectancy:,.0f} | "
                  f"{fmt(r.expectancy_R, d=3)} | {r.trades_per_year:.0f} | {r.avg_hold_days:.1f} | {fmt(r.exposure, True)} | {fmt(r.exposure_adj_return, True)} |")
    sp = split.pivot(index="strategy", columns="split", values="sharpe").loc[names]
    md += ["", "| Strategy | In-sample 2001–15 | Validation 2016–20 | Test 2021–26 |", "|---|---|---|---|"]
    md += [f"| {s} | {fmt(r.in_sample)} | {fmt(r.validation)} | {fmt(r.test)} |" for s, r in sp.iterrows()]
    s = s11[s11.ema == 12]
    md += ["", "| S11 (NQ 5-min) | Split | Trades | Win | Avg R | t | P&L $ | PF |", "|---|---|---|---|---|---|---|---|"]
    md += [f"| {r.cost} | {r.split} | {r.trades} | {fmt(r.win_rate, True)} | {fmt(r.avg_R, d=3)} | {fmt(r.t)} | {r.pnl:,.0f} | {fmt(r.profit_factor)} |" for _, r in s.iterrows()]
    s = s11[(s11.cost == "moderate") & (s11.split == "all")]
    md += ["", "| S11 EMA period | Trades | Avg R | t |", "|---|---|---|---|"] + [f"| {int(r.ema)} | {r.trades} | {fmt(r.avg_R, d=3)} | {fmt(r.t)} |" for _, r in s.iterrows()]
    md += ["", "| Strategy | Turnover (x equity / yr) | Avg margin / equity | Max margin / equity |", "|---|---|---|---|"]
    md += [f"| {k} | {r.turnover_x_per_year:.1f} | {fmt(r.avg_margin_pct, True)} | {fmt(r.max_margin_pct, True)} |" for k, r in TM.loc[names].iterrows()]
    md += ["", "| Strategy (whole contracts, $1M) | Sharpe | CAGR | Trades | Entries skipped (0 contracts) |", "|---|---|---|---|---|"]
    md += [f"| {k} | {fmt(r.sharpe)} | {fmt(r.cagr, True)} | {int(r.trades)} | {int(r.skipped_zero_contracts)} ({fmt(r.skipped_share, True)}) |" for k, r in IA.loc[names].iterrows()]
    Hf = sens.pivot(index="strategy", columns="ema", values="sharpe").loc[names]
    md += ["", "| Full-sample Sharpe (includes the test period) | " + " | ".join(f"EMA {c}" for c in Hf.columns) + " |", "|---" * (len(Hf.columns) + 1) + "|"]
    md += [f"| {k} | " + " | ".join(fmt(v) for v in r.values) + " |" for k, r in Hf.iterrows()]
    open(f"{RES}/report_tables.md", "w", encoding="utf-8").write("\n".join(md))
    print(V[["strategy", "verdict", "passed", "full_sharpe", "test_sharpe", "wf_sharpe", "severe_sharpe", "failed"]].to_string(index=False))


if __name__ == "__main__":
    main()
