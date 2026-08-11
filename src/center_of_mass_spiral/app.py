import numpy as np
from typing import Callable
from .poly_segment import PolySegment, GeometryContext


def get_com_spiral(pseg: PolySegment, density_fn: Callable[[GeometryContext], float | np.ndarray] | None = None) -> tuple[np.ndarray, np.ndarray]:
    if density_fn is None:
        phi = np.column_stack((pseg.C, np.ones(len(pseg))))
    else:
        ctx = pseg.context()
        density = density_fn(ctx)
        if np.isscalar(density):
            density = np.full(len(pseg), float(density))
        phi = np.column_stack(
            (ctx["C"] * density[:, None], density))

    I = pseg.integrate(phi, cumulative=True)
    return I[:, 0] / I[:, 2], I[:, 1] / I[:, 2]
