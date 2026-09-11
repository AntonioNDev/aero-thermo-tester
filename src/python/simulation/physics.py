from __future__ import annotations

import numpy as np


def _unit_vector(v: np.ndarray) -> np.ndarray:
    arr = np.asarray(v, dtype=float)
    return arr / np.linalg.norm(arr)


def dynamic_pressure(rho: float, velocity: np.ndarray) -> float:
    speed = float(np.linalg.norm(np.asarray(velocity, dtype=float)))
    return 0.5 * rho * speed * speed


def cp_max_modified_newtonian(gamma: float, mach: float) -> float:
    gm1 = gamma - 1.0
    gp1 = gamma + 1.0
    m2 = mach * mach
    first = ((gp1 * gp1 * m2) / (4.0 * gamma * m2 - 2.0 * gm1)) ** (gamma / gm1)
    second = (1.0 - gamma + 2.0 * gamma * m2) / gp1
    return (2.0 / (gamma * m2)) * (first * second - 1.0)


def pressure_coefficients(normals: np.ndarray, flow_direction: np.ndarray, gamma: float, mach: float) -> np.ndarray:
    n = np.asarray(normals, dtype=float)
    flow_hat = _unit_vector(flow_direction)
    incidence = np.clip(n @ (-flow_hat), 0.0, 1.0)
    return cp_max_modified_newtonian(gamma=gamma, mach=mach) * np.square(incidence)


def pressure_forces(normals: np.ndarray, areas: np.ndarray, pressure_pa: np.ndarray) -> np.ndarray:
    n = np.asarray(normals, dtype=float)
    a = np.asarray(areas, dtype=float)
    p = np.asarray(pressure_pa, dtype=float)
    return -(p * a)[:, None] * n


def skin_friction_forces(
    areas: np.ndarray,
    flow_direction: np.ndarray,
    rho: float,
    viscosity: float,
    velocity: np.ndarray,
    ref_length_m: float,
) -> tuple[np.ndarray, float]:
    speed = float(np.linalg.norm(np.asarray(velocity, dtype=float)))
    re_l = max((rho * speed * ref_length_m) / viscosity, 1.0)
    cf = 0.074 / (re_l ** 0.2)
    q = dynamic_pressure(rho=rho, velocity=velocity)
    flow_hat = _unit_vector(flow_direction)
    a = np.asarray(areas, dtype=float)
    forces = -(q * cf * a)[:, None] * flow_hat
    return forces, cf


def surface_heating(
    wall_temperature_k: np.ndarray,
    ambient_temperature_k: float,
    mach: float,
    gamma: float,
    recovery_factor: float,
    heat_transfer_coefficient: float,
) -> tuple[float, float, np.ndarray]:
    tw = np.asarray(wall_temperature_k, dtype=float)
    t0 = ambient_temperature_k * (1.0 + 0.5 * (gamma - 1.0) * mach * mach)
    tr = ambient_temperature_k + recovery_factor * (t0 - ambient_temperature_k)
    heat_flux = heat_transfer_coefficient * (tr - tw)
    return t0, tr, heat_flux


def integrate_coefficients(
    total_force: np.ndarray,
    flow_direction: np.ndarray,
    q: float,
    reference_area: float,
    lift_axis: np.ndarray,
) -> dict[str, float]:
    drag_axis = _unit_vector(flow_direction)
    lift_axis_hat = _unit_vector(lift_axis)
    force = np.asarray(total_force, dtype=float)
    drag = float(-force @ drag_axis)
    lift = float(force @ lift_axis_hat)
    denom = q * reference_area
    return {"cd": drag / denom, "cl": lift / denom, "drag_n": drag, "lift_n": lift}
