# Do 12-period EMA strategies work on futures?

> A reproducible test of 12 EMA-based strategies on 13 liquid futures (2001–2026), with pre-registered pass criteria, walk-forward validation and cost stress tests. Brief: `docs/BRIEF.md` · plan and criteria: `docs/PLAN.md`.

## Question
What exactly is being tested, and what result would count as "yes" or "no" (decided before looking at the data).

## Data
- Source:
- Period / market / timeframe:
- How to rebuild it: `python -m casestudy.data ...` (raw data is not committed)

## Method
1. Rules, written so that anyone could reproduce them.
2. Costs and fills (no look-ahead: decisions use only information available at that minute).
3. In-sample vs out-of-sample split, chosen before running anything.

## Results
| | In-sample | Out-of-sample |
|---|---|---|
| Trades | | |
| Win rate | | |
| Avg R | | |
| t-stat | | |

Figures in `results/figures/`.

## Limitations
What this does not show, and how it could be wrong.

## Reproduce
```bash
python -m venv .venv && .venv/Scripts/activate   # Windows
pip install -r requirements.txt
pytest
```
