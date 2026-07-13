"""Shared repo path bootstrap for scripts under /scripts."""

from __future__ import annotations

import sys
from pathlib import Path


def ensure_repo_paths() -> Path:
    """Insert apps/api and repo root into sys.path; return repo root."""
    root = Path(__file__).resolve().parents[1]
    api = root / "apps" / "api"
    for path in (str(api), str(root)):
        if path not in sys.path:
            sys.path.insert(0, path)
    return root
