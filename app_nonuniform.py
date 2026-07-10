from shapes import Ellipse
from polysegment import PolySegment
from plotter import plot_polysegment
import operations
import numpy as np
import matplotlib.pyplot as plt


def weight_fn(s, delta):
    # for unit circle, $\Theta = s$
    rho = 1/(np.pi + s)
    return rho * delta


shape = Ellipse(1, 1, 100)

vl = shape.get_vertex_list()
vl = operations.repeat(vl, 10)

dshape = PolySegment(vl)

cx, cy = dshape.get_com_spiral(weight_fn=weight_fn)

plot_polysegment(dshape, color='black', linewidth=1, alpha=0.5)
plt.plot(cx, cy, 'k-')
plt.axis('equal')
plt.show()
