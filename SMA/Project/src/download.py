"""Data source step: lecture combined table lives on E: (not in Git)."""

from .config import DATA_PATH
from .load_data import resolve_data_path


def ensure_local_dataset() -> str:
    """
    Capstone automation starts from the Module 02 combined parquet
    (YFinance + TA + macro), same file as Module 04 homework.
    Refresh: re-run Module 02 notebook export on your machine.
    """
    path = resolve_data_path(DATA_PATH)
    return str(path)