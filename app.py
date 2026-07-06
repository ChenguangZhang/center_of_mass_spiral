from shapes import Ellipse, NGon, Parabola, Flower
from discrete_shape import DiscreteShape
from plotter import plot_discrete_shape
import operations
import matplotlib.pyplot as plt

shapes = [Ellipse(1, 2, 100), NGon(6, 1), NGon(5, 1), NGon(
    4, 1), NGon(3, 1), Parabola(0, 1, 100), Flower(1, 0.1, 10, 100)]

for shape in shapes:
    vl = shape.get_vertex_list()
    vl = operations.repeat(vl, 10)

    dshape = DiscreteShape(vl)
    dshape.subdivide(10)

    cx, cy = dshape.get_com_spiral()

    plot_discrete_shape(dshape, color='black', linewidth=1, alpha=0.5)
    plt.plot(cx, cy, 'k-')
    plt.axis('equal')
    plt.savefig(f'fig_{vl.name}.png', dpi=300)
