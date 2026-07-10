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

    def get_com_spiral(self, weight_fn: WeightsFunction | None = None) -> Tuple[np.ndarray, np.ndarray]:
        # weight_fn: function that takes segment lengthes and return their weights
        cx = np.array([seg.cx for seg in self.segments])
        cy = np.array([seg.cy for seg in self.segments])
        delta = np.array([seg.delta for seg in self.segments])
        s_vert = np.concatenate(([0], np.cumsum(delta)))
        s = 0.5 * (s_vert[:-1] + s_vert[1:])

        if weight_fn is not None:
            delta = weight_fn(s, delta)

        mass = np.cumsum(delta)
        c_x = np.cumsum(delta*cx) / mass
        c_y = np.cumsum(delta*cy) / mass
        return c_x, c_y
