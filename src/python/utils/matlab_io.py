from __future__ import annotations

from pathlib import Path
from typing import Any

from scipy.io import loadmat, savemat


def save_sweep_input(path: str | Path, payload: dict[str, Any]) -> None:
    savemat(Path(path), payload)


def load_sweep_output(path: str | Path) -> dict[str, Any]:
    data = loadmat(Path(path), simplify_cells=True)
    return {k: v for k, v in data.items() if not k.startswith("__")}
