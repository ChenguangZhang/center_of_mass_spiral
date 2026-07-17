import unittest
import numpy as np
from vertex_list import VertexList
from segment import Segment
from poly_segment import PolySegment, get_com_spiral


class TestDiscreteCircle(unittest.TestCase):
    def setUp(self):
        self.c5 = self.make_circle(5)
        self.c100 = self.make_circle(100)

    def make_circle(self, n):
        vertices = np.array([
            [np.cos(theta), np.sin(theta), theta]
            for theta in np.linspace(0, 2 * np.pi, num=n+1)
        ])
        vl = VertexList(name="Circle" + str(n), vertices=vertices,
                             is_closed=True, is_discrete=True)
        return PolySegment(vl)

    def test_circle_perimeter(self):
        perimeter = self.c5.integrate(1.0)
        ref = np.sin(2*np.pi/(2*5)) * 5*2.0
        np.testing.assert_allclose(perimeter, ref, rtol=1e-2)

    def test_circle_area(self):
        area = self.c100.integrate(
            lambda ctx: ctx["cx"] * ctx["N"][:, 0])
        ref = np.pi
        np.testing.assert_allclose(area, ref, rtol=1e-2)

    def test_circle_loop_integration(self):
        I = self.c100.integrate(
            lambda ctx: ctx["s"][:, np.newaxis] * ctx["T"])
        ref = np.array([2*np.pi, 0.0])
        np.testing.assert_allclose(I, ref, rtol=1e-2, atol=1e-8)


class TestPolySegment(unittest.TestCase):

    def setUp(self):
        # Create a basic vertex list with 3 points, resulting in 2 segments
        # vertices shape is (N, 3), representing (x, y, t)
        vertices = np.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 1.0],
            [1.0, 1.0, 2.0]
        ])
        self.vl = VertexList(name="TestShape", vertices=vertices,
                             is_closed=False, is_discrete=False)
        self.poly = PolySegment(self.vl)

    def test_pythonic_len(self):
        self.assertEqual(len(self.poly), 2)

    def test_pythonic_getitem(self):
        seg0 = self.poly[0]
        self.assertIsInstance(seg0, Segment)
        self.assertEqual((seg0.x1, seg0.y1), (0.0, 0.0))

        # Test negative indexing
        seg_last = self.poly[-1]
        self.assertEqual((seg_last.x2, seg_last.y2), (1.0, 1.0))

    def test_pythonic_iter(self):
        segments_from_loop = []
        for seg in self.poly:
            segments_from_loop.append(seg)
            self.assertIsInstance(seg, Segment)

        self.assertEqual(len(segments_from_loop), 2)
        self.assertIs(segments_from_loop[0], self.poly[0])
        self.assertIs(segments_from_loop[1], self.poly[1])

    def test_subdivide_non_discrete(self):
        self.poly.subdivide(n=2)
        self.assertEqual(len(self.poly), 4)

    def test_subdivide_discrete_skipped(self):
        discrete_vl = VertexList(
            name="TestDiscrete", vertices=self.vl.vertices, is_closed=False, is_discrete=True)
        discrete_poly = PolySegment(discrete_vl)
        # Subdivision shouldn't change the number of segments
        discrete_poly.subdivide(n=5)
        self.assertEqual(len(discrete_poly), 2)

    def test_integrate_1d_cumulative(self):
        # Two equal-length segments (length 1.0 each)
        # Values at segment midpoints: [2.0, 4.0]
        # Expected cumulative weighted average: [2.0, 3.0]
        values = np.array([2.0, 4.0])
        result = self.poly.integrate(values, cumulative=True)
        np.testing.assert_allclose(result, [2.0, 6.0])

    def test_integrate_1d_default_total(self):
        values = np.array([2.0, 4.0])
        result = self.poly.integrate(values)
        np.testing.assert_allclose(result, 6.0)

    def test_integrate_2d_cumulative(self):
        # Two equal-length segments; 2D values
        # Values: [[1.0, 2.0], [3.0, 4.0]]
        # Expected cumulative weighted avg: [[1.0, 2.0], [2.0, 3.0]]
        values = np.array([[1.0, 2.0], [3.0, 4.0]])
        result = self.poly.integrate(values, cumulative=True)
        np.testing.assert_allclose(result, [[1.0, 2.0], [4.0, 6.0]])

    def test_integrate_2d_total(self):
        values = np.array([[1.0, 2.0], [3.0, 4.0]])
        result = self.poly.integrate(values)
        np.testing.assert_allclose(result, [4.0, 6.0])

    def test_integrate_with_weighted_callable(self):
        values = np.array([2.0, 4.0])
        result = self.poly.integrate(lambda ctx: 2.0 * values, cumulative=True)
        np.testing.assert_allclose(result, [4.0, 12.0])

    def test_integrate_callable_returns_scalar(self):
        result = self.poly.integrate(lambda ctx: 2.0, cumulative=True)
        np.testing.assert_allclose(result, [2.0, 4.0])

    def test_integrate_scalar_total(self):
        result = self.poly.integrate(2.0)
        np.testing.assert_allclose(result, 4.0)

    def test_integrate_callable_returns_1d(self):
        result = self.poly.integrate(
            lambda ctx: np.array([2.0, 4.0]), cumulative=True
        )
        np.testing.assert_allclose(result, [2.0, 6.0])

    def test_integrate_callable_returns_2d(self):
        result = self.poly.integrate(
            lambda ctx: np.array([[1.0, 2.0], [3.0, 4.0]]),
            cumulative=True,
        )
        np.testing.assert_allclose(result, [[1.0, 2.0], [4.0, 6.0]])

    def test_integrate_callable_uses_context_s(self):
        # Midpoint arclengths are [0.5, 1.5] for two unit segments.
        result = self.poly.integrate(lambda ctx: ctx["s"], cumulative=True)
        np.testing.assert_allclose(result, [0.5, 2.0])

    def test_integrate_callable_wrong_shape_raises(self):
        with self.assertRaises(ValueError):
            self.poly.integrate(lambda ctx: np.array([1.0, 2.0, 3.0]))

    def test_integrate_callable_non_numeric_output_raises(self):
        with self.assertRaises(TypeError):
            self.poly.integrate(np.array(["not", "numeric"]))

    def test_integrate_callable_matches_direct_array(self):
        values = np.array([2.0, 4.0])
        direct = self.poly.integrate(values)
        via_callable = self.poly.integrate(lambda ctx: values)
        np.testing.assert_allclose(via_callable, direct)

    def test_get_com_spiral(self):
        # Segment 0: (0,0)→(1,0), cx=0.5, cy=0.0, length=1.0
        # Segment 1: (1,0)→(1,1), cx=1.0, cy=0.5, length=1.0
        cx, cy = get_com_spiral(self.poly)
        np.testing.assert_allclose(cx, [0.5, 0.75])
        np.testing.assert_allclose(cy, [0.0, 0.25])


if __name__ == '__main__':
    unittest.main()
