import hashlib
import json
import subprocess
import sys
import numpy as np
import pandas as pd
import scipy
import sklearn
import yaml
from pathlib import Path


def get_git_sha(repo_dir: Path | None = None) -> str:
    """Return short git commit SHA or 'unknown'."""
    try:
        cmd = ["git", "rev-parse", "--short", "HEAD"]
        res = subprocess.run(cmd, cwd=repo_dir, capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception:
        return "uncommitted_or_no_git"


def compute_config_hash(config_paths: list[Path]) -> str:
    """Compute sha256 hash over combined YAML configs."""
    hasher = hashlib.sha256()
    for p in sorted(config_paths):
        if p.exists():
            with open(p, "rb") as f:
                hasher.update(f.read())
    return hasher.hexdigest()[:12]


def get_provenance_metadata(config_dir: Path | None = None) -> dict[str, str]:
    """Gather complete execution environment provenance."""
    cfg_paths = list(config_dir.glob("*.yaml")) if config_dir and config_dir.exists() else []
    return {
        "git_sha": get_git_sha(),
        "config_hash": compute_config_hash(cfg_paths),
        "python_version": sys.version.split()[0],
        "numpy_version": np.__version__,
        "scipy_version": scipy.__version__,
        "pandas_version": pd.__version__,
        "sklearn_version": sklearn.__version__,
    }
