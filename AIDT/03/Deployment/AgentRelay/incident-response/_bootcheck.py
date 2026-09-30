import sys
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "observability" / "bootcheck.txt"
p.write_text("start\n", encoding="utf-8")
try:
    p.write_text("import main\n", encoding="utf-8")
    import main  # noqa: F401
    p.write_text("import-ok\n", encoding="utf-8")
except Exception as exc:
    p.write_text(f"fail:{exc}\n", encoding="utf-8")
    sys.exit(1)
