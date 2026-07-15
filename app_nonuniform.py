from shapes import Ellipse
from poly_segment import PolySegment, get_com_spiral
from plotter import plot_polysegment
import operations
import numpy as np
import matplotlib.pyplot as plt


def density_fn(ctx):
    return 1/(np.pi + ctx["s"])


shape = Ellipse(1, 1, 100)

vl = shape.get_vertex_list()
vl = operations.repeat(vl, 10)

pseg = PolySegment(vl)

cx, cy = get_com_spiral(pseg, density_fn=density_fn)

plot_polysegment(pseg, color='black', linewidth=1, alpha=0.5)
plt.plot(cx, cy, 'k-')
plt.axis('equal')
plt.show()
