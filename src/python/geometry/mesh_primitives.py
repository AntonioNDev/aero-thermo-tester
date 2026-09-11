from __future__ import annotations

import numpy as np


def _face_geometry(vertices: np.ndarray, faces: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    tri = vertices[faces]
    e1 = tri[:, 1] - tri[:, 0]
    e2 = tri[:, 2] - tri[:, 0]
    cross = np.cross(e1, e2)
    area2 = np.linalg.norm(cross, axis=1)
    normals = cross / np.maximum(area2[:, None], 1e-12)
    areas = 0.5 * area2
    centroids = np.mean(tri, axis=1)
    return normals, areas, centroids


def make_box_mesh(width: float = 1.0, height: float = 1.0, depth: float = 1.0) -> dict:
    w = width / 2.0
    h = height / 2.0
    d = depth / 2.0
    vertices = np.array(
        [
            [-w, -h, -d],
            [w, -h, -d],
            [w, h, -d],
            [-w, h, -d],
            [-w, -h, d],
            [w, -h, d],
            [w, h, d],
            [-w, h, d],
        ],
        dtype=float,
    )
    faces = np.array(
        [
            [0, 1, 2], [0, 2, 3],
            [4, 6, 5], [4, 7, 6],
            [0, 4, 5], [0, 5, 1],
            [1, 5, 6], [1, 6, 2],
            [2, 6, 7], [2, 7, 3],
            [3, 7, 4], [3, 4, 0],
        ],
        dtype=int,
    )
    normals, areas, centroids = _face_geometry(vertices, faces)
    return {
        "vertices": vertices,
        "faces": faces,
        "face_normals": normals,
        "face_areas": areas,
        "face_centroids": centroids,
        "face_curvature": np.zeros(faces.shape[0], dtype=float),
    }
