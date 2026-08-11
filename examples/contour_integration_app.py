from center_of_mass_spiral import Ellipse
from center_of_mass_spiral.app import contour_integrate
import numpy as np

shape = Ellipse(2, 2, 32, theta_start=0, theta_end=np.pi)
residual = contour_integrate(shape, '1/(1+z**2)**2')

relative_error = np.abs(residual - np.pi/2.0) / (np.pi/2.0)
print(f"Complex integration result: {residual}")
print(f"Relative error: {relative_error:.2e}")
