import numpy as np
from vertex_list import VertexList
from segment import Segment
from typing import Callable, Tuple

WeightsFunction = Callable[[np.ndarray, np.ndarray], np.ndarray]


class PolySegment:
    def __init__(self, vertex_list: VertexList):
        self.vertex_list = vertex_list
        self.segments: list[Segment] = []
        for i in range(len(vertex_list.vertices)-1):
            x1, y1, t1 = vertex_list.vertices[i]
            x2, y2, t2 = vertex_list.vertices[i+1]
            self.segments.append(Segment(x1, y1, x2, y2))

    def __len__(self):
        return len(self.segments)

    def __getitem__(self, index):
        return self.segments[index]

    def __iter__(self):
        return iter(self.segments)

    def subdivide(self, n):
        if self.vertex_list.is_discrete:
            # when defining, say, a parabola via a list of vertices, the spacing between the vertices
            # are already small, so 99% of the time we don't want to subdivide it any further
            print(
                f"Warning: skip subdividing discrete shape {self.vertex_list.name}")
            return
        new_segments = []
        for segment in self.segments:
            new_segs = segment.subdivide(n)
            new_segments.extend(new_segs)
        self.segments = new_segments

    def integrate(self, values: np.ndarray, weight_fn: WeightsFunction | None = None) -> np.ndarray:
        """Compute the cumulative weighted average of values over the segments.

        Args:
            values: Array of values at each segment midpoint. Shape (N,) for
                scalar values or (N, D) for D-dimensional values.
            weight_fn: Optional function that takes arc-length positions ``s``
                and segment lengths ``delta`` and returns per-segment weights.
                When ``None``, segment lengths are used as weights.

        Returns:
            Array with the same shape as ``values`` containing the cumulative
            weighted average up to each segment.
        """
        values = np.asarray(values)
        delta = np.array([seg.delta for seg in self.segments])
        s_vert = np.concatenate(([0], np.cumsum(delta)))
        s = 0.5 * (s_vert[:-1] + s_vert[1:])

        weights = weight_fn(s, delta) if weight_fn is not None else delta

        cumulative_weights = np.cumsum(weights)
        if values.ndim == 1:
            return np.cumsum(weights * values) / cumulative_weights
        else:
            return np.cumsum(weights[:, np.newaxis] * values, axis=0) / cumulative_weights[:, np.newaxis]
