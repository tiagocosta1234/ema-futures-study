"""Download free 1-minute BID candles from Dukascopy's public datafeed into a parquet file.

    python -m casestudy.data USATECHIDXUSD 2025-11-01 2026-10-31 data/raw/nq_m1.parquet

Instruments: USATECHIDXUSD (Nasdaq 100), DEUIDXEUR (DAX 40), USA500IDXUSD (S&P 500), XAUUSD (gold, price scale differs).
Index CFD prices are stored x1000 in the feed; `load()` divides them back. Timestamps are UTC.
Requests are slow and polite on purpose (the feed throttles parallel downloads)."""
import datetime as dt
import lzma
import os
import struct
import sys
import time
import urllib.request

import pandas as pd

URL = "https://datafeed.dukascopy.com/datafeed/{ins}/{y}/{m:02d}/{d:02d}/BID_candles_min_1.bi5"


def fetch_day(ins, day, tries=3):
    url = URL.format(ins=ins, y=day.year, m=day.month - 1, d=day.day)
    for _ in range(tries):
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read()
            break
        except Exception:
            time.sleep(2)
    else:
        return None
    if not raw:
        return None
    data = lzma.decompress(raw)
    rows = [struct.unpack(">5if", data[i:i + 24]) for i in range(0, len(data), 24)]
    df = pd.DataFrame(rows, columns=["t", "o", "c", "l", "h", "v"])
    df["t"] = pd.Timestamp(day, tz="UTC") + pd.to_timedelta(df.t, unit="s")
    return df.set_index("t")[["o", "h", "l", "c", "v"]]


def download(ins, start, end, out, pause=0.4, rounds=4):
    days = [start + dt.timedelta(k) for k in range((end - start).days + 1)]
    days = [d for d in days if d.weekday() < 5]
    have = pd.read_parquet(out) if os.path.exists(out) else None
    for _ in range(rounds):
        got = set(have.index.normalize().date) if have is not None else set()
        missing = [d for d in days if d not in got]
        print(f"missing days: {len(missing)}", flush=True)
        if not missing:
            break
        parts = []
        for d in missing:
            p = fetch_day(ins, d)
            if p is not None:
                parts.append(p)
            time.sleep(pause)
        if parts:
            have = pd.concat(([have] if have is not None else []) + parts).sort_index()
            have = have[~have.index.duplicated()]
            have.to_parquet(out)
    return have


def load(path, scale=1000.0, tz="America/New_York"):
    df = pd.read_parquet(path)[["o", "h", "l", "c"]] / scale
    df.index = df.index.tz_convert(tz)
    return df


if __name__ == "__main__":
    ins, a, b, out = sys.argv[1], dt.date.fromisoformat(sys.argv[2]), dt.date.fromisoformat(sys.argv[3]), sys.argv[4]
    download(ins, a, b, out)
