import numpy as np

from geometry.mesh_primitives import make_box_mesh
from simulation.pipeline import run_facewise_simulation


def test_facewise_pipeline_shapes_and_coefficients():
    mesh = make_box_mesh()
    settings = {
        "flow": {
            "gamma": 1.4,
            "density_kg_m3": 1.225,
            "viscosity_pa_s": 1.7894e-5,
            "temperature_k": 288.15,
        },
        "heating": {
            "recovery_factor": 0.89,
            "heat_transfer_coefficient_w_m2k": 35.0,
        },
    }

    out = run_facewise_simulation(
        mesh=mesh,
        flow_direction=np.array([1.0, 0.0, 0.0]),
        velocity=np.array([200.0, 0.0, 0.0]),
        mach=0.6,
        settings=settings,
        wall_temperature_k=np.full(mesh["faces"].shape[0], 300.0),
        lift_axis=np.array([0.0, 1.0, 0.0]),
    )

    n_faces = mesh["faces"].shape[0]
    assert out["cp"].shape == (n_faces,)
    assert out["face_pressure_pa"].shape == (n_faces,)
    assert out["pressure_force_n"].shape == (n_faces, 3)
    assert out["skin_friction_force_n"].shape == (n_faces, 3)
    assert out["heat_flux_w_m2"].shape == (n_faces,)
    assert "cd" in out["coefficients"] and "cl" in out["coefficients"]
