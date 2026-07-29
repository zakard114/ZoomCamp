"""ONNX embedder shim — drop-in when sentence-transformers/PyTorch fails on Windows."""
from __future__ import annotations

import sys
from pathlib import Path

_EMBED_DIR = Path(__file__).resolve().parent.parent / "embed"
_MODEL_DIR = _EMBED_DIR / "models" / "Xenova" / "all-MiniLM-L6-v2"

if str(_EMBED_DIR) not in sys.path:
    sys.path.insert(0, str(_EMBED_DIR))

from embedder import Embedder  # noqa: E402


class SentenceTransformer:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        del model_name  # course uses all-MiniLM-L6-v2 ONNX export only
        self._embedder = Embedder(path=_MODEL_DIR)

    def encode(self, sentences, normalize_embeddings: bool = True, **kwargs):
        del kwargs
        if isinstance(sentences, str):
            return self._embedder.encode(sentences, normalize=normalize_embeddings)
        return self._embedder.encode_batch(list(sentences), normalize=normalize_embeddings)
