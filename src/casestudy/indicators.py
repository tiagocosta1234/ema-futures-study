"""Indicators. Every value at bar t uses only bars <= t (no look-ahead)."""
import numpy as np
import pandas as pd


def ema(s, n):
    return s.ewm(span=n, adjust=False, min_periods=n).mean()


def atr(d, n=14):
    tr = pd.concat([d.high - d.low, (d.high - d.close.shift()).abs(), (d.low - d.close.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()


def cross_up(a, b):
    return (a > b) & (a.shift(1) <= b.shift(1))


def cross_down(a, b):
    return (a < b) & (a.shift(1) >= b.shift(1))
