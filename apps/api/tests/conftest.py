"""pytest configuration for SignalHub API tests."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
API = ROOT / "apps" / "api"
for path in (str(API), str(ROOT)):
    if path not in sys.path:
        sys.path.insert(0, path)

pytest_plugins = []
