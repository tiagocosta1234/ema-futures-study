"""Fill docs/REPORT_TEMPLATE.md with the tables from results/report_tables.md -> REPORT.md."""
import os

ROOT = os.path.join(os.path.dirname(__file__), "..")
blocks = open(os.path.join(ROOT, "results/report_tables.md"), encoding="utf-8").read().split("\n\n")
verdicts, _, failed, full, splits, s11, s11_ema, turnover, integer, fullsens = blocks[:10]
t = open(os.path.join(ROOT, "docs/REPORT_TEMPLATE.md"), encoding="utf-8").read()
for k, v in {"TABLE_VERDICTS": verdicts, "FAILED": failed, "TABLE_FULL": full, "TABLE_SPLITS": splits,
             "TABLE_S11": s11 + "\n\n" + s11_ema, "TABLE_TURNOVER": turnover, "TABLE_INTEGER": integer,
             "TABLE_FULLSENS": fullsens}.items():
    t = t.replace("{{" + k + "}}", v)
open(os.path.join(ROOT, "REPORT.md"), "w", encoding="utf-8").write(t)
print("REPORT.md written")
