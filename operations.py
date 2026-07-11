import numpy as np
from vertex_list import VertexList
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from poly_segment import PolySegment, DensityFunction


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


def get_com_spiral(pseg: 'PolySegment', density_fn: 'DensityFunction | None' = None) -> tuple[np.ndarray, np.ndarray]:
    centers = np.array([[seg.cx, seg.cy] for seg in pseg.segments])
    result = pseg.integrate(centers, density_fn)
    return result[:, 0], result[:, 1]
