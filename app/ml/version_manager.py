# ---------------------------------------------------------------------------
# app/ml/version_manager.py
# Compatibility shim — the authoritative VersionManager lives in
# app.continuous_learning.version_manager.
# ---------------------------------------------------------------------------
from app.continuous_learning.version_manager import VersionManager  # noqa: F401

__all__ = ["VersionManager"]