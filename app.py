from shapes import Ellipse, NGon, Parabola, Flower
from poly_segment import PolySegment, get_com_spiral
from plotter import plot_polysegment
import operations
import matplotlib.pyplot as plt

shapes = [
    NGon(3, 1),
    NGon(4, 1),
    NGon(6, 1),
    Ellipse(2, 1, 100),
    Flower(1, 0.5, 10, 500),
    Parabola(0, 1, 100)
]

plt.figure(figsize=(12, 8))
for i, shape in enumerate(shapes):
    vl = shape.get_vertex_list()
    vl = operations.repeat(vl, 10)

    pseg = PolySegment(vl)
    pseg.subdivide(10)

    cx, cy = get_com_spiral(pseg)

    plt.subplot(2, 3, i + 1)
    plot_polysegment(pseg, ax=plt.gca(), color='black', linewidth=1, alpha=0.5)
    plt.plot(cx, cy, 'k-')
    plt.axis('equal')

plt.tight_layout()
plt.show()
