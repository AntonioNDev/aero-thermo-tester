from __future__ import annotations

import numpy as np


def pressure_gradient_proxy(pressures: np.ndarray, centroid_positions: np.ndarray) -> np.ndarray:
    p = np.asarray(pressures, dtype=float)
    c = np.asarray(centroid_positions, dtype=float)
    centered = c - np.mean(c, axis=0, keepdims=True)
    radial = np.linalg.norm(centered, axis=1)
    return np.abs(p - np.mean(p)) / np.maximum(radial, 1e-9)
