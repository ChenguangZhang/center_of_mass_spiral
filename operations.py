import numpy as np
from vertexlist import VertexList
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from polysegment import PolySegment, WeightsFunction


def repeat(vl: VertexList, num_loop: int) -> VertexList:
    if not vl.is_closed:
        print(
            f"Warning: skip repeating vertex list {vl.name}, return original")
        return vl
    else:
        vertices = vl.vertices.copy()
        vertices = vertices[:-1]
        vertices = np.tile(vertices, (num_loop, 1))
        vertices = np.vstack((vertices, vertices[0]))
        return VertexList(
            name=vl.name + f'_repeat_{num_loop}',
            vertices=vertices,
            is_closed=vl.is_closed,
            is_discrete=vl.is_discrete
        )


def get_com_spiral(pseg: 'PolySegment', weight_fn: 'WeightsFunction | None' = None) -> tuple[np.ndarray, np.ndarray]:
    """Return the center-of-mass spiral coordinates for a PolySegment.

    Extracts segment midpoint coordinates and delegates to
    :meth:`PolySegment.integrate` to compute the cumulative weighted average.

    Args:
        pseg: The poly-segment path to integrate over.
        weight_fn: Optional density function passed to ``pseg.integrate``.

    Returns:
        A tuple ``(cx, cy)`` where each element is a 1-D array of length N
        containing the cumulative center-of-mass x and y coordinates.
    """
    centers = np.array([[seg.cx, seg.cy] for seg in pseg.segments])
    result = pseg.integrate(centers, weight_fn)
    return result[:, 0], result[:, 1]
