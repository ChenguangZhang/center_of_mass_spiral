import numpy as np
from vertex_list import VertexList
from segment import Segment


class DiscreteShape:
    def __init__(self, vertex_list: VertexList):
        self.vertex_list = vertex_list
        self.segments: list[Segment] = []
        for i in range(len(vertex_list.vertices)-1):
            x1, y1, t1 = vertex_list.vertices[i]
            x2, y2, t2 = vertex_list.vertices[i+1]
            self.segments.append(Segment(x1, y1, x2, y2))

    def subdivide(self, n):
        new_segments = []
        for segment in self.segments:
            new_segs = segment.subdivide(n)
            new_segments.extend(new_segs)
        self.segments = new_segments

    def get_com_spiral(self):
        cx = np.array([seg.cx for seg in self.segments])
        cy = np.array([seg.cy for seg in self.segments])
        delta = np.array([seg.delta for seg in self.segments])

        mass = np.cumsum(delta)
        c_x = np.cumsum(delta*cx) / mass
        c_y = np.cumsum(delta*cy) / mass
        return c_x, c_y
