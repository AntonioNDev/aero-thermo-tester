import numpy as np

from analysis.pressure_gradient import pressure_gradient_proxy
from analysis.weak_points import flag_weak_points, weak_point_score


def test_weak_point_scoring_and_thresholding():
    pressures = np.array([100.0, 120.0, 500.0, 110.0])
    centroids = np.array(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.2, 0.0, 0.0], [0.5, 0.0, 0.0]],
        dtype=float,
    )
    grad = pressure_gradient_proxy(pressures, centroids)
    curvature = np.array([0.0, 0.1, 0.9, 0.2])

    score = weak_point_score(grad, curvature, gradient_weight=0.6, curvature_weight=0.4)
    weak = flag_weak_points(score, threshold=0.65)

    assert score.shape == (4,)
    assert weak.dtype == np.bool_
    assert weak[2]
