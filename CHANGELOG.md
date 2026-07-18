# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-07-17

### Added
- Initial release of the center_of_mass_spiral library
- Core `PolySegment` class for representing polygonal curves
- Generic `integrate()` method with support for:
  - Scalar, array, and callable integrands
  - Cumulative and total integration modes
  - Multi-dimensional integrand arrays
- `get_com_spiral()` function for computing center of mass spirals
- Support for non-uniform density functions
- Built-in shapes: `Ellipse`, `NGon`, `Parabola`, `Flower`
- Geometric context with arc length, centers, tangents, and normals
- Comprehensive test suite with 22+ tests
- Modern Python packaging with `pyproject.toml`
- GitHub Actions CI workflow
- Example applications demonstrating library usage

### Project Structure
- Adopted modern Python project structure with `src/` layout
- Separated library code, examples, and tests into distinct directories
- Added GitHub Actions for continuous integration
- Comprehensive documentation and examples

[0.1.0]: https://github.com/ChenguangZhang/center_of_mass_spiral/releases/tag/v0.1.0
