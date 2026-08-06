from center_of_mass_spiral import (
    Ellipse,
    PolySegment,
    plot_polysegment, close
)
import numpy as np
import matplotlib.pyplot as plt

shape = Ellipse(2, 2, 32, theta_start=0, theta_end=np.pi)
vl = shape.get_vertex_list()
vl = close(vl)
pseg = PolySegment(vl)


def complex_integrand(ctx):
    # ref: Example 1 at https://en.wikipedia.org/wiki/Contour_integration
    z = ctx["C"][:, 0] + 1j * ctx["C"][:, 1]
    return 1.0/(1 + z**2)**2


residual = pseg.integrate(complex_integrand, is_complex=True)
relative_error = np.abs(residual - np.pi/2.0) / (np.pi/2.0)
print(f"Complex integration result: {residual}")
print(f"Relative error: {relative_error:.2e}")

plt.figure(figsize=(6, 4))
plot_polysegment(pseg, ax=plt.gca(), show_detail=True,
                 color='black', linewidth=1, alpha=0.5)
plt.axis('equal')
plt.tight_layout()
plt.show()
