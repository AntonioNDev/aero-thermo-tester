from __future__ import annotations

import numpy as np

from analysis.pressure_gradient import pressure_gradient_proxy
from analysis.weak_points import flag_weak_points, generate_suggestions, weak_point_score
from simulation.pipeline import run_facewise_simulation


def run_analysis(mesh: dict, settings: dict, flow_direction: np.ndarray, velocity: np.ndarray, mach: float, wall_temperature_k: np.ndarray) -> dict:
    sim = run_facewise_simulation(
        mesh=mesh,
        flow_direction=flow_direction,
        velocity=velocity,
        mach=mach,
        settings=settings,
        wall_temperature_k=wall_temperature_k,
        lift_axis=np.array([0.0, 1.0, 0.0]),
    )

    gradient = pressure_gradient_proxy(sim["face_pressure_pa"], np.asarray(mesh["face_centroids"], dtype=float))
    curvature = np.asarray(mesh.get("face_curvature", np.zeros_like(gradient)), dtype=float)

    cfg = settings["analysis"]
    score = weak_point_score(
        pressure_gradient=gradient,
        curvature=curvature,
        gradient_weight=float(cfg["weak_point_gradient_weight"]),
        curvature_weight=float(cfg["weak_point_curvature_weight"]),
    )
    weak = flag_weak_points(score=score, threshold=float(cfg["weak_point_threshold"]))

    return {
        "simulation": sim,
        "weak_point_score": score,
        "weak_point_mask": weak,
        "suggestions": generate_suggestions(score=score, weak_mask=weak),
    }
