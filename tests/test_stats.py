import numpy as np
from casestudy.stats import summary


def test_summary_basic():
    s = summary([1, -1, 2, -1])
    assert s["trades"] == 4
    assert s["win_rate"] == 0.5
    assert np.isclose(s["avg_r"], 0.25)
    assert s["max_dd"] == -1.0


def test_summary_empty():
    assert summary([])["trades"] == 0
