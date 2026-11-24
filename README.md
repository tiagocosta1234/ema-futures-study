# Case study: <title>

> One-line question this study answers.

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
