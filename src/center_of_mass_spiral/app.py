import numpy as np
from typing import Callable
from .poly_segment import PolySegment, GeometryContext
from .vertex_list import VertexList
from .operations import close
from .shapes import Shape


def get_com_spiral(pseg: PolySegment, density_fn: Callable[[GeometryContext], float | np.ndarray] | None = None) -> tuple[np.ndarray, np.ndarray]:
    if density_fn is None:
        phi = np.column_stack((pseg.C, np.ones(len(pseg))))
    else:
        ctx = pseg.context()
        density = density_fn(ctx)
        if np.isscalar(density):
            density = np.full(len(pseg), float(density))
        phi = np.column_stack(
            (ctx["C"] * density[:, None], density))

    I = pseg.integrate(phi, cumulative=True)
    return I[:, 0] / I[:, 2], I[:, 1] / I[:, 2]


def parse_complex_integrand(expr: str) -> Callable[[GeometryContext], np.ndarray]:
    """
    Parse a string expression in `z` into a complex integrand callable.

    The variable `z = x + i*y` is constructed automatically from the
    segment centroid coordinates in the geometry context.

    Parameters
    ----------
    expr
        A Python expression string involving `z`, e.g. ``"1/(1+z**2)**2"``.

    Returns
    -------
    Callable[[GeometryContext], np.ndarray]
        A function suitable for passing to ``PolySegment.integrate(..., is_complex=True)``.

    Examples
    --------
    >>> f = parse_complex_integrand("1/(1+z**2)**2")
    >>> pseg.integrate(f, is_complex=True)
    """
    code = compile(expr, "<string>", "eval")

    def integrand(ctx: GeometryContext) -> np.ndarray:
        z = ctx["C"][:, 0] + 1j * ctx["C"][:, 1]
        return eval(code, {"__builtins__": {}}, {"z": z, "np": np, "exp": np.exp,
                                                 "sin": np.sin, "cos": np.cos,
                                                 "log": np.log, "sqrt": np.sqrt,
                                                 "pi": np.pi, "e": np.e})
    return integrand


def contour_integrate(
    path: Shape | VertexList | PolySegment,
    expr: str,
    *,
    auto_close: bool = True,
    subdivide: int | None = None
) -> complex | np.ndarray:
    """
    Evaluate a complex contour integral along a path.

    Parameters
    ----------
    path
        The integration contour. Can be a ``Shape``, a ``VertexList``,
        or an already-built ``PolySegment``.
    expr
        A Python expression string in ``z``, e.g. ``"1/(1+z**2)**2"``.
    auto_close
        If ``True`` (default) and the path is not already closed, close it
        automatically before integrating.
    subdivide
        If given, call ``pseg.subdivide(n)`` to refine the path.

    Returns
    -------
    complex | np.ndarray
        The contour integral  ∮ f(z) dz.

    Examples
    --------
    >>> from center_of_mass_spiral import Ellipse, contour_integrate
    >>> result = contour_integrate(Ellipse(2, 2, 128), "1/(1+z**2)**2")
    >>> result          # ≈ π/2  (residue theorem)
    """
    from .shapes import Shape  # local import avoids circular dependency

    if isinstance(path, PolySegment):
        pseg = path
    else:
        if isinstance(path, Shape):
            vl = path.get_vertex_list()
        else:
            vl = path  # VertexList

        if auto_close and not vl.is_closed:
            vl = close(vl)

        pseg = PolySegment(vl)

    if subdivide is not None:
        pseg.subdivide(subdivide)

    integrand = parse_complex_integrand(expr)
    return pseg.integrate(integrand, cumulative=False, is_complex=True)
