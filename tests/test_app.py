import unittest
import numpy as np
from center_of_mass_spiral import VertexList, PolySegment, get_com_spiral


class TestGetComSpiral(unittest.TestCase):

    def setUp(self):
        vertices = np.array([
            [0.0, 0.0],
            [1.0, 0.0],
            [1.0, 1.0]
        ])
        vl = VertexList(name="TestShape", vertices=vertices,
                        is_closed=False, is_discrete=False)
        self.poly = PolySegment(vl)

    def test_get_com_spiral(self):
        # Segment 0: (0,0)→(1,0), c=(0.5, 0.0), length=1.0
        # Segment 1: (1,0)→(1,1), c=(1.0, 0.5), length=1.0
        cx, cy = get_com_spiral(self.poly)
        np.testing.assert_allclose(cx, [0.5, 0.75])
        np.testing.assert_allclose(cy, [0.0, 0.25])


if __name__ == '__main__':
    unittest.main()
