"""
Jupyter / scripts: load OPENAI_API_KEY from LLM/.env (not CWD).

Usage in a notebook (first cell):

    from openai_env import get_openai_client
    client = get_openai_client()
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

_LLM_ROOT = Path(__file__).resolve().parent.parent.parent
_ENV_FILE = _LLM_ROOT / ".env"


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
    """Return OpenAI client using the key from LLM/.env."""
    from openai import OpenAI

    return OpenAI(api_key=load_openai_key())
