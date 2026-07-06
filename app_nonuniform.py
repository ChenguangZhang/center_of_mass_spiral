from shapes import Ellipse
from discrete_shape import DiscreteShape
from plotter import plot_discrete_shape
import operations
import numpy as np
import matplotlib.pyplot as plt


def weight_fn(delta):
    # for unit circle, $Theta$ is arc-length
    Theta = np.cumsum(delta)
    rho = 1/(np.pi + Theta)
    return rho * delta


shape = Ellipse(1, 1, 100)

vl = shape.get_vertex_list()
vl = operations.repeat(vl, 10)

dshape = DiscreteShape(vl)

cx, cy = dshape.get_com_spiral(weight_fn=weight_fn)

plot_discrete_shape(dshape, color='black', linewidth=1, alpha=0.5)
plt.plot(cx, cy, 'k-')
plt.axis('equal')
plt.show()
