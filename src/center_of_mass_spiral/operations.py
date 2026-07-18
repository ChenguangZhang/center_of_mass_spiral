import numpy as np
from .vertex_list import VertexList


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
