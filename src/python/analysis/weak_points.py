from __future__ import annotations

import numpy as np


def weak_point_score(pressure_gradient: np.ndarray, curvature: np.ndarray, gradient_weight: float, curvature_weight: float) -> np.ndarray:
    g = np.asarray(pressure_gradient, dtype=float)
    c = np.asarray(curvature, dtype=float)

    g_norm = (g - np.min(g)) / max(np.ptp(g), 1e-12)
    c_norm = (c - np.min(c)) / max(np.ptp(c), 1e-12)

    return gradient_weight * g_norm + curvature_weight * c_norm


def flag_weak_points(score: np.ndarray, threshold: float) -> np.ndarray:
    return np.asarray(score, dtype=float) >= threshold


def generate_suggestions(score: np.ndarray, weak_mask: np.ndarray) -> list[str]:
    s = np.asarray(score, dtype=float)
    mask = np.asarray(weak_mask, dtype=bool)

    high = np.where(mask & (s >= 0.85))[0]
    medium = np.where(mask & (s < 0.85))[0]

    out: list[str] = []
    if high.size:
        out.append(f"Round or fillet faces near indices: {high.tolist()}")
    if medium.size:
        out.append(f"Review local smoothing near faces: {medium.tolist()}")
    if not out:
        out.append("No weak points above current threshold.")
    return out
