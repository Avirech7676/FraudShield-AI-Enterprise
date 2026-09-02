"""
Model Version Management module.
Manages semantic versioning and tracking for trained ML models.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class VersionManager:
    """Manages model versions and metadata tracking."""

    def __init__(self, metadata_dir: str = "models/metadata"):
        self.metadata_dir = Path(metadata_dir)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)
        self.version_history_file = self.metadata_dir / "version_history.json"
        self._init_history()

    def _init_history(self) -> None:
        """Initialize version history file if it doesn't exist."""
        if not self.version_history_file.exists():
            self._save_history({"versions": [], "current_version": None})

    def _load_history(self) -> Dict[str, Any]:
        """Load version history from JSON."""
        try:
            with open(self.version_history_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"versions": [], "current_version": None}

    def _save_history(self, history: Dict[str, Any]) -> None:
        """Save version history to JSON."""
        with open(self.version_history_file, "w") as f:
            json.dump(history, f, indent=2)

    def get_current_version(self) -> Optional[str]:
        """Get the current active model version string."""
        history = self._load_history()
        return history.get("current_version")

    def bump_version(
        self,
        metrics: Dict[str, float],
        model_path: str,
        bump_type: str = "patch",
        description: str = "",
    ) -> str:
        """Bump model version and record metadata."""
        history = self._load_history()
        current = history.get("current_version")

        if not current:
            new_version = "1.0.0"
        else:
            parts = [int(p) for p in current.split(".")]
            if bump_type == "major":
                parts[0] += 1
                parts[1] = 0
                parts[2] = 0
            elif bump_type == "minor":
                parts[1] += 1
                parts[2] = 0
            else:
                parts[2] += 1
            new_version = f"{parts[0]}.{parts[1]}.{parts[2]}"

        record = {
            "version": new_version,
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": metrics,
            "model_path": model_path,
            "description": description,
        }

        history["versions"].append(record)
        history["current_version"] = new_version
        self._save_history(history)

        logger.info(f"Model version bumped to {new_version}")
        return new_version

    def get_history(self) -> List[Dict[str, Any]]:
        """Return all recorded version entries."""
        history = self._load_history()
        return history.get("versions", [])
