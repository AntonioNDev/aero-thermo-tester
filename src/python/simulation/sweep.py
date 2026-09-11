from __future__ import annotations

import numpy as np

from simulation.pipeline import run_facewise_simulation


def sweep_numpy(
    mesh: dict,
    speeds: np.ndarray,
    flow_directions: np.ndarray,
    mach_values: np.ndarray,
    settings: dict,
    wall_temperature_k: np.ndarray,
    lift_axis: np.ndarray,
) -> dict:
    speeds = np.asarray(speeds, dtype=float)
    flow_directions = np.asarray(flow_directions, dtype=float)
    mach_values = np.asarray(mach_values, dtype=float)

    velocity_vectors = speeds[:, None] * flow_directions

    sims = [
        run_facewise_simulation(
            mesh=mesh,
            flow_direction=flow_directions[i],
            velocity=velocity_vectors[i],
            mach=mach_values[i],
            settings=settings,
            wall_temperature_k=wall_temperature_k,
            lift_axis=lift_axis,
        )
        for i in range(speeds.shape[0])
    ]

    return {
        "cd": np.asarray([s["coefficients"]["cd"] for s in sims]),
        "cl": np.asarray([s["coefficients"]["cl"] for s in sims]),
        "drag_n": np.asarray([s["coefficients"]["drag_n"] for s in sims]),
        "lift_n": np.asarray([s["coefficients"]["lift_n"] for s in sims]),
    }
