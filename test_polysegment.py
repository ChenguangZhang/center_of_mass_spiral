import unittest
import numpy as np
from vertex_list import VertexList
from segment import Segment
from poly_segment import PolySegment, get_com_spiral
import operations


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

    def test_integrate_1d(self):
        # Two equal-length segments (length 1.0 each)
        # Values at segment midpoints: [2.0, 4.0]
        # Expected cumulative weighted average: [2.0, 3.0]
        values = np.array([2.0, 4.0])
        result = self.poly.integrate(values)
        np.testing.assert_allclose(result, [2.0, 6.0])

    def test_integrate_2d(self):
        # Two equal-length segments; 2D values
        # Values: [[1.0, 2.0], [3.0, 4.0]]
        # Expected cumulative weighted avg: [[1.0, 2.0], [2.0, 3.0]]
        values = np.array([[1.0, 2.0], [3.0, 4.0]])
        result = self.poly.integrate(values)
        np.testing.assert_allclose(result, [[1.0, 2.0], [4.0, 6.0]])

    def test_integrate_with_density_fn(self):
        # density_fn doubles weights
        def density_fn(s):
            return 2.0
        values = np.array([2.0, 4.0])
        result = self.poly.integrate(values, density_fn=density_fn)
        np.testing.assert_allclose(result, [4.0, 12.0])

    def test_get_com_spiral(self):
        # Segment 0: (0,0)→(1,0), cx=0.5, cy=0.0, length=1.0
        # Segment 1: (1,0)→(1,1), cx=1.0, cy=0.5, length=1.0
        cx, cy = get_com_spiral(self.poly)
        np.testing.assert_allclose(cx, [0.5, 0.75])
        np.testing.assert_allclose(cy, [0.0, 0.25])


if __name__ == '__main__':
    unittest.main()
