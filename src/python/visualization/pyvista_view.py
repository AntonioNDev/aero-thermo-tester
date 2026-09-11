from __future__ import annotations

import numpy as np


def colorize_mesh(polydata, scalar_name: str, values: np.ndarray):
    polydata = polydata.copy()
    polydata.cell_data[scalar_name] = np.asarray(values, dtype=float)
    return polydata
