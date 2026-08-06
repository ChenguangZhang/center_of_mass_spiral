import numpy as np
from .vertex_list import VertexList


def _get_average_segment_length(vertices: np.ndarray) -> float:
    """Calculate average distance between consecutive vertices."""
    if len(vertices) < 2:
        raise ValueError(
            "At least two vertices are required to calculate average segment length.")

    delta = np.diff(vertices, axis=0)
    return np.mean(np.sum(delta**2, axis=1))**0.5


def _interpolate_vertices(v1: np.ndarray, v2: np.ndarray,
                          distance_threshold: float) -> list[np.ndarray]:
    distance = np.linalg.norm(v2 - v1)

    if distance <= distance_threshold:
        return []

    n = int(np.ceil(distance / distance_threshold))
    increment = (v2 - v1) / n

    # Create n-1 intermediate points
    intermediate = []
    for i in range(1, n):
        intermediate.append(v1 + i * increment)
    return intermediate


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
            name=vl.name + f'/repeat_{num_loop}',
            vertices=vertices,
            is_closed=vl.is_closed,
            is_discrete=vl.is_discrete,
            num_repeat=num_loop
        )


def reverse(vl: VertexList) -> VertexList:
    vertices = vl.vertices.copy()
    vertices = vertices[::-1]

    return VertexList(
        name=vl.name + '/reversed',
        vertices=vertices,
        is_closed=vl.is_closed,
        is_discrete=vl.is_discrete,
        num_repeat=vl.num_repeat
    )


def append(vl: VertexList, vertex: np.ndarray, refine: bool = True) -> VertexList:
    vertex = np.atleast_1d(vertex).flatten()
    if vertex.shape[0] != len(vl.vertices[0]):
        raise ValueError(
            f"Vertex must have {len(vl.vertices[0])} coordinates, got shape {vertex.shape}")

    if vl.is_closed:
        print(
            f"Warning: cannot append to closed vertex list {vl.name}, return original")
        return vl

    vertices = vl.vertices.copy()
    last_vertex = vertices[-1]

    # Optionally refine by inserting intermediate vertices
    new_vertices = [vertices]
    if refine:
        threshold = _get_average_segment_length(vertices)
        intermediate = _interpolate_vertices(last_vertex, vertex, threshold)
        if intermediate:
            new_vertices.append(np.array(intermediate))

    # Append the new vertex
    new_vertices.append(vertex.reshape(1, len(vl.vertices[0])))
    vertices = np.vstack(new_vertices)

    return VertexList(
        name=vl.name + '/append',
        vertices=vertices,
        is_closed=False,
        is_discrete=vl.is_discrete,
        num_repeat=1
    )


def prepend(vl: VertexList, vertex: np.ndarray, refine: bool = True) -> VertexList:
    # Validate vertex shape
    vertex = np.atleast_1d(vertex).flatten()
    if vertex.shape[0] != len(vl.vertices[0]):
        raise ValueError(
            f"Vertex must have {len(vl.vertices[0])} coordinates, got shape {vertex.shape}")

    # Can't prepend to closed shapes
    if vl.is_closed:
        print(
            f"Warning: cannot prepend to closed vertex list {vl.name}, return original")
        return vl

    vertices = vl.vertices.copy()
    first_vertex = vertices[0]

    # Optionally refine by inserting intermediate vertices
    new_vertices = [vertex.reshape(1, len(vl.vertices[0]))]
    if refine:
        threshold = _get_average_segment_length(vertices)
        intermediate = _interpolate_vertices(vertex, first_vertex, threshold)
        if intermediate:
            new_vertices.append(np.array(intermediate))

    # Add existing vertices
    new_vertices.append(vertices)
    vertices = np.vstack(new_vertices)

    return VertexList(
        name=vl.name + '/prepend',
        vertices=vertices,
        is_closed=False,
        is_discrete=vl.is_discrete,
        num_repeat=1
    )


def close(vl: VertexList, refine: bool = True) -> VertexList:
    if vl.is_closed:
        print(
            f"Warning: vertex list {vl.name} is already closed, return original")
        return vl

    vertices = vl.vertices.copy()
    first_vertex = vertices[0]
    last_vertex = vertices[-1]

    # Check if already closed (within tolerance)
    if np.allclose(first_vertex, last_vertex, atol=1e-10):
        # Already closed geometrically, just mark as closed
        return VertexList(
            name=vl.name + '/closed',
            vertices=vertices,
            is_closed=True,
            is_discrete=vl.is_discrete,
            num_repeat=vl.num_repeat
        )

    # Need to add closing vertex
    new_vertices = [vertices]
    if refine:
        threshold = _get_average_segment_length(vertices)
        intermediate = _interpolate_vertices(
            last_vertex, first_vertex, threshold)
        if intermediate:
            new_vertices.append(np.array(intermediate))

    # Add closing vertex (duplicate of first)
    new_vertices.append(first_vertex.reshape(1, len(vl.vertices[0])))
    vertices = np.vstack(new_vertices)

    return VertexList(
        name=vl.name + '/closed',
        vertices=vertices,
        is_closed=True,
        is_discrete=vl.is_discrete,
        num_repeat=vl.num_repeat
    )


def join(vl1: VertexList, vl2: VertexList, refine: bool = True) -> VertexList:
    if vl1.is_closed:
        raise ValueError(
            f"Cannot join closed vertex list {vl1.name}. Both vertex lists must be open.")
    if vl2.is_closed:
        raise ValueError(
            f"Cannot join closed vertex list {vl2.name}. Both vertex lists must be open.")

    # Validate is_discrete flags match
    if vl1.is_discrete != vl2.is_discrete:
        raise ValueError(
            f"Cannot join vertex lists with different is_discrete flags: "
            f"{vl1.name} (is_discrete={vl1.is_discrete}) and "
            f"{vl2.name} (is_discrete={vl2.is_discrete})")

    vertices1 = vl1.vertices.copy()
    vertices2 = vl2.vertices.copy()

    # Check if last vertex of vl1 equals first vertex of vl2 (within tolerance)
    last_v1 = vertices1[-1]
    first_v2 = vertices2[0]

    new_vertices = [vertices1]

    if np.allclose(last_v1, first_v2, atol=1e-10):
        # Remove duplicate - skip first vertex of vl2
        vertices2 = vertices2[1:]
        if len(vertices2) == 0:
            # vl2 only had one vertex which was duplicate, just return vl1
            return VertexList(
                name=f'{vl1.name}+{vl2.name}',
                vertices=vertices1,
                is_closed=False,
                is_discrete=vl1.is_discrete,
                num_repeat=1
            )
        first_v2 = vertices2[0]

    # Optionally refine the connection
    if refine:
        threshold = _get_average_segment_length(vertices1)
        intermediate = _interpolate_vertices(last_v1, first_v2, threshold)
        if intermediate:
            new_vertices.append(np.array(intermediate))

    # Append second vertex list
    new_vertices.append(vertices2)
    vertices = np.vstack(new_vertices)

    return VertexList(
        name=f'{vl1.name}+{vl2.name}',
        vertices=vertices,
        is_closed=False,
        is_discrete=vl1.is_discrete,
        num_repeat=1
    )
