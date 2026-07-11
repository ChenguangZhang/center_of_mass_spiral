import unittest
import numpy as np
from vertex_list import VertexList
from segment import Segment
from polysegment import PolySegment


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

    def test_get_com_spiral(self):
        c_x, c_y = self.poly.get_com_spiral()

        np.testing.assert_allclose(c_x, np.array([0.5, 0.75]))
        np.testing.assert_allclose(c_y, np.array([0.0, 0.25]))

    def test_get_com_spiral_with_weights(self):
        def weight_fn(s, delta):
            return delta * (1 + s)

        c_x, c_y = self.poly.get_com_spiral(weight_fn=weight_fn)

        np.testing.assert_allclose(c_x, np.array([0.5, 13.0 / 16.0]))
        np.testing.assert_allclose(c_y, np.array([0.0, 5.0 / 16.0]))


if __name__ == '__main__':
    unittest.main()
