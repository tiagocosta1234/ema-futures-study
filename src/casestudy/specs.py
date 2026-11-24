"""Contract specifications (CME/CBOT/NYMEX/COMEX standard contracts).

point_value: USD per 1.0 move of the quoted price.  tick: minimum price increment.
margin: approximate initial margin per contract in 2026 (USD), used only for the margin cap.
slip_ticks: base slippage per side, in ticks (1 for the most liquid, 2 for the rest).
"""
SPECS = {
    #        class        point_value   tick        margin  slip_ticks
    "ES": ("equity",      50.0,         0.25,       25000, 1),
    "NQ": ("equity",      20.0,         0.25,       35000, 1),
    "YM": ("equity",       5.0,         1.0,        18000, 1),
    "CL": ("energy",    1000.0,         0.01,        7000, 2),
    "NG": ("energy",   10000.0,         0.001,       5000, 2),
    "GC": ("metals",     100.0,         0.1,        18000, 1),
    "SI": ("metals",    5000.0,         0.005,      20000, 2),
    "HG": ("metals",   25000.0,         0.0005,      8000, 2),
    "6E": ("fx",      125000.0,         0.00005,     3000, 1),
    "6J": ("fx",    12500000.0,         0.0000005,   4000, 1),
    "6B": ("fx",       62500.0,         0.0001,      3500, 1),
    "ZB": ("rates",     1000.0,         1 / 32,      5000, 1),
    "ZN": ("rates",     1000.0,         1 / 64,      2500, 1),
}
COMMISSION = 2.50  # USD per contract per side, commission + exchange + NFA fees (conservative retail)


def spec(sym):
    c, pv, tick, margin, slip = SPECS[sym]
    return dict(asset_class=c, point_value=pv, tick=tick, margin=margin, slip_ticks=slip)
