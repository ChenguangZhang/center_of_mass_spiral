import numpy as np
from vertex_list import VertexList


def repeat(vl: VertexList, num_loop: int) -> VertexList:
    """
    Repeat the vertex list `vl` for `num_loop` times.
    """
    vertices = vl.vertices
    if vl.is_closed:
        vertices = vertices[:-1]  # remove the last vertex to avoid duplication
    vertices = np.tile(vertices, (num_loop, 1))
    if vl.is_closed:
        vertices = np.vstack((vertices, vertices[0]))  # close the polygon
    return VertexList(
        name=vl.name + f'_repeat_{num_loop}',
        vertices=vertices,
        is_closed=vl.is_closed,
        is_discrete=vl.is_discrete
    )
