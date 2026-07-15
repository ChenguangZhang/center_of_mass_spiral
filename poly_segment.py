import numpy as np
from vertex_list import VertexList
from segment import Segment
from typing import Callable

GeometryContext = dict[str, np.ndarray]


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

    def context(self) -> GeometryContext:
        return {
            "s": self.s,
            "cx": self.cx,
            "cy": self.cy,
            "delta": self.delta,
            "index": np.arange(len(self.segments))
        }

    def _normalize_integrand(
        self,
        phi: float |
        np.ndarray |
        Callable[[GeometryContext], float | np.ndarray]
    ) -> float | np.ndarray:
        if callable(phi):
            phi = phi(self.context())

        if isinstance(phi, (int, float)):
            return float(phi)
        elif isinstance(phi, np.ndarray):
            if phi.shape[0] != len(self.segments):
                raise ValueError(
                    f"Integrand array must have a leading dimension of {len(self.segments)}, but got {phi.shape[0]}."
                )
            return phi
        else:
            raise TypeError(
                "Integrand must be a number, a numpy array, or a callable returning one of those.")

    def integrate(self, phi: float | np.ndarray | Callable[[GeometryContext], float | np.ndarray]) -> np.ndarray:
        """
        Do
        $$
            \int_0^s phi(c, s', ...) ds'
        $$
        using the trapezoidal rule (i.e., integrand evaluated at segment centers)

        Parameters
        ----------
        phi
            Integrand. Supported forms:
            - single number
            - np.array with shape (N,) or (N, ...), where N = len(segments)
            - callable: phi(context) -> numeric scalar or numpy array with leading shape (N, ...)

        Returns
        -------
        np.ndarray
            Cumulative integral values sampled at each segment center:
            - scalar phi -> shape (N,)
            - phi shape (N,) -> shape (N,)
            - phi shape (N, ...) -> shape (N, ...)

        Examples
        --------
        >>> pseg.integrate(2.0)
        >>> pseg.integrate(np.array([1.0, 2.0, 3.0]))
        >>> pseg.integrate(lambda ctx: ctx["s"])
        >>> pseg.integrate(lambda ctx: np.stack([ctx["cx"], ctx["cy"]], axis=1))
        """

        ds = self.delta

        phi_value = self._normalize_integrand(phi)

        if isinstance(phi_value, float):
            return np.cumsum(ds) * phi_value

        assert isinstance(phi_value, np.ndarray)

        if phi_value.ndim == 1:
            return np.cumsum(ds * phi_value)
        else:
            weight_shape = (len(ds),) + (1,) * (phi_value.ndim - 1)
            weighted = ds.reshape(weight_shape) * phi_value
            return np.cumsum(weighted, axis=0)


def get_com_spiral(pseg: 'PolySegment', density_fn: Callable[[GeometryContext], float | np.ndarray] | None = None) -> tuple[np.ndarray, np.ndarray]:
    if density_fn is None:
        phi = np.array([[seg.cx, seg.cy, 1.0] for seg in pseg.segments])
    else:
        ctx = pseg.context()
        density = density_fn(ctx)
        phi = np.column_stack(
            (ctx["cx"] * density, ctx["cy"] * density, np.ones_like(ctx["s"])*density))

    I = pseg.integrate(phi)
    return I[:, 0] / I[:, 2], I[:, 1] / I[:, 2]
