"""
Jupyter / scripts: always load OPENAI_API_KEY from this repo's .env (not CWD).

Usage in a notebook (first cell):

    from openai_env import get_openai_client
    client = get_openai_client()
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

_REPO_ROOT = Path(__file__).resolve().parent
_ENV_FILE = _REPO_ROOT / ".env"
_VENV_PYTHON = (_REPO_ROOT / ".venv" / "Scripts" / "python.exe").resolve()


def _assert_llm_venv() -> None:
    """Fail fast if Jupyter is not using LLM\\.venv (wrong kernel → wrong env / old keys)."""
    if not _VENV_PYTHON.is_file():
        return
    cur = Path(sys.executable).resolve()
    try:
        ok = cur == _VENV_PYTHON or os.path.samefile(cur, _VENV_PYTHON)
    except OSError:
        ok = cur == _VENV_PYTHON
    if not ok:
        raise RuntimeError(
            "Jupyter 커널이 LLM\\.venv 가 아닙니다.\n"
            f"  현재: {cur}\n"
            f"  필요: {_VENV_PYTHON}\n"
            '우측 상단 커널에서 "Python (LLM-Zoomcamp)" 선택 후 Kernel → Restart.'
        )


def load_openai_key() -> str:
    """Load .env from LLM folder with override=True; return stripped API key."""
    load_dotenv(_ENV_FILE, override=True)
    key = (os.environ.get("OPENAI_API_KEY") or "").strip()
    if not key:
        raise RuntimeError(
            f"OPENAI_API_KEY is empty. Set it in {_ENV_FILE} (one line, no quotes)."
        )
    os.environ["OPENAI_API_KEY"] = key
    return key


def get_openai_client():
    """Return OpenAI client using the key from this repo's .env (explicit api_key, no stale env)."""
    _assert_llm_venv()
    from openai import OpenAI

    return OpenAI(api_key=load_openai_key())
