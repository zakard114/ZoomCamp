#!/usr/bin/env python3
"""Write EDA summary + correlation figure for rubric evidence."""

import json
import os
import sys

os.environ.setdefault("MPLCONFIGDIR", r"E:\IT_SPACES\AI\.cache\matplotlib")
os.environ.setdefault("XDG_CACHE_HOME", r"E:\IT_SPACES\AI\.cache")

from src.modeling import build_labeled_frame
from src.eda import run_eda_report


def main() -> int:
    frame, features = build_labeled_frame()
    report = run_eda_report(frame, features)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())