import numpy as np
from vertex_list import VertexList
from segment import Segment
from typing import Callable, Tuple

DensityFunction = Callable[[np.ndarray], np.ndarray]


class PolySegment:
    def __init__(self, vertex_list: VertexList):
        self.vertex_list = vertex_list
        self.segments: list[Segment] = []
        for i in range(len(vertex_list.vertices)-1):
            x1, y1, t1 = vertex_list.vertices[i]
            x2, y2, t2 = vertex_list.vertices[i+1]
            self.segments.append(Segment(x1, y1, x2, y2))
        self.__update_geometric_properties()

    def __update_geometric_properties(self):
        self.cx = np.array([seg.cx for seg in self.segments])
        self.cy = np.array([seg.cy for seg in self.segments])
        self.delta = np.array([seg.delta for seg in self.segments])
        s_vert = np.concatenate(([0], np.cumsum(self.delta)))
        self.s = 0.5 * (s_vert[:-1] + s_vert[1:])

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
        self.__update_geometric_properties()

    def integrate(self, phi: float | np.ndarray, density_fn: DensityFunction | None = None) -> np.ndarray:
        # Do $\int_0^s phi(c, s', ...) \cdot rho(s') \cdot ds'$ using the trapezoidal rule

        if density_fn is not None:
            rho_ds = density_fn(self.s) * self.delta
        else:
            rho_ds = self.delta

        if isinstance(phi, float):
            return np.cumsum(rho_ds) * phi
        elif isinstance(phi, np.ndarray):
            assert phi.shape[0] == len(
                self.segments), "phi must have the same length as the number of segments"

            if phi.ndim == 1:
                return np.cumsum(rho_ds * phi)
            else:
                return np.cumsum(rho_ds[:, np.newaxis] * phi, axis=0)
        else:
            raise TypeError("phi must be a float or a numpy array")


def get_com_spiral(pseg: 'PolySegment', density_fn: 'DensityFunction | None' = None) -> tuple[np.ndarray, np.ndarray]:
    centers = np.array([[seg.cx, seg.cy] for seg in pseg.segments])
    nume = pseg.integrate(centers, density_fn)
    deno = pseg.integrate(1.0, density_fn)
    result = nume / deno[:, np.newaxis]
    return result[:, 0], result[:, 1]
