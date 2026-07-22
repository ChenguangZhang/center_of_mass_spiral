"""Center of Mass Spiral - A library for computing center of mass spirals for 2D curves."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("center_of_mass_spiral")
except PackageNotFoundError:
    # Package is not installed, use a default version
    __version__ = "unknown"

from center_of_mass_spiral.vertex_list import VertexList
from center_of_mass_spiral.segment import Segment
from center_of_mass_spiral.poly_segment import PolySegment, get_com_spiral, GeometryContext
from center_of_mass_spiral.operations import repeat
from center_of_mass_spiral.shapes import Ellipse, NGon, Parabola, Flower, Shape
from center_of_mass_spiral.plotter import plot_polysegment

__all__ = [
    "__version__",
    "VertexList",
    "Segment",
    "PolySegment",
    "get_com_spiral",
    "GeometryContext",
    "repeat",
    "Ellipse",
    "NGon",
    "Parabola",
    "Flower",
    "Shape",
    "plot_polysegment",
]
