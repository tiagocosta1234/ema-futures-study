# Do 12-period EMA strategies work on futures?

> A reproducible test of 12 EMA-based strategies on 13 liquid futures (2001–2026), with pre-registered pass criteria, walk-forward validation and cost stress tests. Brief: `docs/BRIEF.md` · plan and criteria: `docs/PLAN.md`.

## Result in one paragraph
**One of 12 strategies passed all six criteria fixed before the test, and only narrowly: S06 Triple EMA (12/26/50)**, with test-period Sharpe 0.35 vs a 0.30 bar, positive in 12/13 markets and 5/5 asset classes, and surviving 3× costs. Data and engine fixes were made after the test was seen (disclosed), so it is a candidate to confirm on new data, not a proven edge. The 12-period EMA on its own is too fast for daily futures: price/EMA crosses lose after realistic costs (Sharpe −0.45 to −0.69), and almost every strategy improves with slower EMAs (50–100). Full report: **[REPORT.md](REPORT.md)**.

![equity](results/figures/equity_curves.png)

## How it was done
- 13 futures (equity, energy, metals, FX, rates), daily bars Sep 2000 – Nov 2026, roll-adjusted (`docs/DATA.md`); NQ 5-min for the intraday strategy.
- 12 strategies (`docs/STRATEGIES.md`), one engine: next-open fills, commissions + slippage, 0.5% risk sizing, portfolio and asset-class risk caps, margin cap, daily loss limit.
- Pass criteria and splits written before any run (`docs/PLAN.md`); locked 2021–26 test; walk-forward; EMA 8–100 sensitivity; 1×/2×/3× cost stress; regime breakdowns.
- Tests include a no-look-ahead check (changing the future must not change past signals).

## Reproduce
```bash
pip install -r requirements.txt
python scripts/run_all.py && python scripts/make_report.py && python scripts/build_report.py
pytest
```

## Layout
`src/casestudy/` code · `scripts/` pipeline · `results/` tables and figures · `docs/` brief, plan, data notes, strategy spec · `tests/`.

*Built with AI-assisted development; research design, review and decisions by me.*

*Hypothetical backtested results; not investment advice.*
