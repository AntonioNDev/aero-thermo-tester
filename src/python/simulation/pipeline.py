from __future__ import annotations

import numpy as np

from simulation.physics import (
    dynamic_pressure,
    integrate_coefficients,
    pressure_coefficients,
    pressure_forces,
    skin_friction_forces,
    surface_heating,
)


def run_facewise_simulation(
    mesh: dict,
    flow_direction: np.ndarray,
    velocity: np.ndarray,
    mach: float,
    settings: dict,
    wall_temperature_k: np.ndarray,
    lift_axis: np.ndarray,
) -> dict:
    normals = np.asarray(mesh["face_normals"], dtype=float)
    areas = np.asarray(mesh["face_areas"], dtype=float)

    rho = float(settings["flow"]["density_kg_m3"])
    gamma = float(settings["flow"]["gamma"])
    viscosity = float(settings["flow"]["viscosity_pa_s"])

    cps = pressure_coefficients(normals=normals, flow_direction=flow_direction, gamma=gamma, mach=mach)
    q = dynamic_pressure(rho=rho, velocity=velocity)
    face_pressures = q * cps
    fp = pressure_forces(normals=normals, areas=areas, pressure_pa=face_pressures)

    ref_length_m = float(np.cbrt(np.sum(areas)))
    ff, cf = skin_friction_forces(
        areas=areas,
        flow_direction=flow_direction,
        rho=rho,
        viscosity=viscosity,
        velocity=velocity,
        ref_length_m=ref_length_m,
    )

    heating = settings["heating"]
    t0, tr, qdot = surface_heating(
        wall_temperature_k=wall_temperature_k,
        ambient_temperature_k=float(settings["flow"]["temperature_k"]),
        mach=mach,
        gamma=gamma,
        recovery_factor=float(heating["recovery_factor"]),
        heat_transfer_coefficient=float(heating["heat_transfer_coefficient_w_m2k"]),
    )

    total_face_forces = fp + ff
    total_force = np.sum(total_face_forces, axis=0)
    coeffs = integrate_coefficients(
        total_force=total_force,
        flow_direction=flow_direction,
        q=q,
        reference_area=float(np.sum(areas)),
        lift_axis=lift_axis,
    )

    return {
        "cp": cps,
        "face_pressure_pa": face_pressures,
        "pressure_force_n": fp,
        "skin_friction_force_n": ff,
        "cf": cf,
        "t0_k": t0,
        "tr_k": tr,
        "heat_flux_w_m2": qdot,
        "total_force_n": total_force,
        "coefficients": coeffs,
    }
