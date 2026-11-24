import numpy as np
import pandas as pd

from casestudy.engine import Config, run
from casestudy.strategies import STRATEGIES
from casestudy.prep import roll_adjust


def _toy(n=400, seed=0):
    rng = np.random.default_rng(seed)
    c = 100 + np.cumsum(rng.normal(0, 1, n))
    o = np.r_[c[0], c[:-1]] + rng.normal(0, 0.2, n)
    h = np.maximum(o, c) + rng.random(n)
    l = np.minimum(o, c) - rng.random(n)
    idx = pd.bdate_range("2010-01-01", periods=n)
    return pd.DataFrame(dict(open=o, high=h, low=l, close=c), index=idx)


def test_signals_have_no_lookahead():
    """Changing the future must not change any signal in the past."""
    d = _toy()
    cut = 250
    d2 = d.copy()
    d2.iloc[cut:, :] = d2.iloc[cut:, :] * 1.5 + 7
    for name, f in STRATEGIES.items():
        a, b = f(d), f(d2)
        cols = ["long_entry", "short_entry", "long_exit", "short_exit"]
        assert a[cols].iloc[:cut].equals(b[cols].iloc[:cut]), name


def test_engine_runs_and_costs_reduce_equity():
    d = roll_adjust(_toy())
    data = {"ES": d}
    sig = {"ES": STRATEGIES["S01 Price/EMA cross"](d)}
    e1, t1 = run(data, sig, Config(cost_mult=1))
    e3, t3 = run(data, sig, Config(cost_mult=3))
    assert len(t1) > 5
    assert e3.iloc[-1] < e1.iloc[-1]


def test_roll_gap_is_removed():
    d = _toy(100)
    d.index = pd.bdate_range("2010-01-04", periods=len(d))
    k = d.index.get_loc(d.index[d.index.day == 20][2])  # a day inside CL's monthly roll window
    d.iloc[k:, :] += 40  # artificial roll gap
    adj = roll_adjust(d, "CL")
    assert adj.roll.sum() >= 1
    assert adj.roll.iloc[k]
    assert abs(adj.open.iloc[k] - adj.close.iloc[k - 1]) < 5
