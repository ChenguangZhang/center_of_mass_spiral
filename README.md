# Center of Mass Spiral

A Python library for computing center of mass spirals for 2D curves with support for various shapes and non-uniform density distributions.

## Features

- **Flexible curve representation**: Define curves using vertices, parametric shapes, or discrete points
- **Generic integration framework**: Compute cumulative or total integrals along curves
- **Non-uniform density support**: Calculate center of mass with arbitrary density functions
- **Built-in shapes**: Ellipse, N-gon, Parabola, Flower, and more
- **Visualization tools**: Plot curves and their center of mass spirals

## Installation

### From source (development)

```bash
git clone https://github.com/ChenguangZhang/center_of_mass_spiral.git
cd center_of_mass_spiral
pip install -e ".[dev]"
```

## Quick Start

```python
from center_of_mass_spiral import Ellipse, PolySegment, get_com_spiral, plot_polysegment, repeat
import matplotlib.pyplot as plt

# Create an ellipse shape
shape = Ellipse(2, 1, 100)
vl = shape.get_vertex_list()
vl = repeat(vl, 10)  # Repeat the curve 10 times

# Create a polysegment and compute center of mass spiral
pseg = PolySegment(vl)
cx, cy = get_com_spiral(pseg)

# Visualize
plot_polysegment(pseg, color='black', linewidth=1, alpha=0.5)
plt.plot(cx, cy, 'r-', linewidth=2)
plt.axis('equal')
plt.show()
```

## Advanced Usage

### Custom Density Functions

```python
import numpy as np

def density_fn(ctx):
    """Non-uniform density that varies with arc length."""
    return 1 / (np.pi + ctx["s"])

cx, cy = get_com_spiral(pseg, density_fn=density_fn)
```

### Generic Integration

The `integrate` method supports flexible integration along curves:

```python
# Integrate a constant
total_length = pseg.integrate(1.0)

# Integrate an array (per-segment values)
values = np.array([...])  # Shape: (n_segments,) or (n_segments, ...)
result = pseg.integrate(values, cumulative=True)

# Integrate using a callable with geometric context
result = pseg.integrate(
    lambda ctx: ctx["c"][:, 0] * ctx["N"][:, 0],  # Area calculation
    cumulative=False
)
```

Available context keys:
- `"s"`: Arc length at segment centers
- `"c"`: Center positions, shape `(n, 2)`
- `"delta"`: Segment lengths
- `"T"`: Tangent vectors, shape `(n, 2)`
- `"N"`: Normal vectors, shape `(n, 2)`
- `"index"`: Segment indices

## Examples

See the `examples/` directory for more examples:
- `basic_shapes.py`: Center of mass spirals for various geometric shapes
- `nonuniform_density.py`: Center of mass with non-uniform density

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Running Tests with Coverage

```bash
pytest tests/ --cov=center_of_mass_spiral --cov-report=term-missing
```

## Project Structure

```
center_of_mass_spiral/
├── src/center_of_mass_spiral/  # Library code
├── examples/                    # Example applications
├── tests/                       # Unit tests
├── docs/                        # Documentation
└── pyproject.toml              # Project configuration
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Citation

If you use this library in your research, please cite:

```bibtex
@software{center_of_mass_spiral,
  author = {Zhang, Chenguang},
  title = {Center of Mass Spiral: A library for computing center of mass spirals for 2D curves},
  year = {2026},
  url = {https://github.com/ChenguangZhang/center_of_mass_spiral}
}
```
