import numpy as np
import matplotlib.pyplot as plt

from center_of_mass_spiral import Shape, PolySegment, get_com_spiral, plot_polysegment, VertexList


class Archimedean(Shape):
    def __init__(self, theta_max, n):
        self.theta_max = theta_max
        self.n = n

        t = np.linspace(0, self.theta_max, self.n+1)
        self.xy = np.vstack((t * np.cos(t), t * np.sin(t), t)).T

    def get_vertex_list(self) -> VertexList:
        return VertexList(
            name="Archimedis-" + str(self.n),
            vertices=self.xy,
            is_closed=False,
            is_discrete=True
        )


shape = Archimedean(6*np.pi, 500)
pseg = PolySegment(shape.get_vertex_list())
cx, cy = get_com_spiral(pseg)

plot_polysegment(pseg, color='black', linewidth=1, alpha=0.5)
plt.plot(cx, cy, 'r-')
plt.axis('equal')
plt.show()
