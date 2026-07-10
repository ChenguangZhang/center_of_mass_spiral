from shapes import Ellipse, NGon, Parabola, Flower
from polysegment import PolySegment
from plotter import plot_polysegment
import operations
import matplotlib.pyplot as plt

shapes = [Ellipse(1, 2, 100), NGon(6, 1), NGon(5, 1), NGon(
    4, 1), NGon(3, 1), Parabola(0, 1, 100), Flower(1, 0.1, 10, 100)]

for shape in shapes:
    vl = shape.get_vertex_list()
    vl = operations.repeat(vl, 10)

    pseg = PolySegment(vl)
    pseg.subdivide(10)

    cx, cy = operations.get_com_spiral(pseg)

    plot_polysegment(pseg, color='black', linewidth=1, alpha=0.5)
    plt.plot(cx, cy, 'k-')
    plt.axis('equal')
    plt.savefig(f'fig_{vl.name}.png', dpi=300)
