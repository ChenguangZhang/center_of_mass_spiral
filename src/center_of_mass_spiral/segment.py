import numpy as np


class Segment:
    def __init__(self, a, b, length=None):
        self.a = a
        self.b = b
        self.C = (a + b) * 0.5
        if length is not None:
            self.delta = length
        else:
            self.delta = self.__length()

        deltav = b - a
        self.T = deltav / self.delta
        if len(a) == 2:
            self.N = np.array([self.T[1], -self.T[0]])

    def __length(self):
        deltav = self.b - self.a
        return np.linalg.norm(deltav)

    def subdivide(self, n):
        '''
        uniformly divide 1 segment into n segments
        |---------------| =>
        |-|-|-|-|-|-|-|-|
        '''
        inc = (self.b - self.a) / n
        delta_n = self.delta / n
        new_segments = []
        for i in range(n):
            new_segments.append(
                Segment(self.a + i * inc, self.a + (i + 1) * inc, length=delta_n))
        return new_segments

    def __repr__(self):
        return f'Segment({self.a} to {self.b})'
