from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import joblib
from loguru import logger


def setup_logger(level: str = "INFO") -> None:
    """Configure loguru logger once."""
    logger.remove()
    logger.add(sys.stderr, level=level)


def ensure_dir(path: str | Path) -> Path:
    """Create directory if it does not exist."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def save_json(obj: dict[str, Any], path: str | Path) -> Path:
    """Save a dictionary as a JSON file."""
    path = Path(path)
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    return path


def load_json(path: str | Path) -> dict[str, Any]:
    """Load JSON content from a file."""
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def save_joblib(obj: Any, path: str | Path) -> Path:
    """Save an object using joblib."""
    path = Path(path)
    ensure_dir(path.parent)
    joblib.dump(obj, path)
    return path


def load_joblib(path: str | Path) -> Any:
    """Load an object from a joblib file."""
    return joblib.load(Path(path))


def timestamp() -> str:
    """Generate UTC timestamp string."""
    return datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")


def project_meta() -> dict[str, Any]:
    """Collect minimal environment metadata."""
    import platform

    return {
        "python_version": platform.python_version(),
        "timestamp_utc": timestamp(),
    }
