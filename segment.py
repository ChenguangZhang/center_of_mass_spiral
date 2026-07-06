import numpy as np


class Segment:
    def __init__(self, x1, y1, x2, y2, length=None):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.cx = (x1 + x2) / 2
        self.cy = (y1 + y2) / 2
        if length is not None:
            self.delta = length
        else:
            self.delta = self.__length()

    def __length(self):
        return np.sqrt((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2)

    def subdivide(self, n):
        '''
        uniformly divide 1 segment into n segments
        |---------------| =>
        |-|-|-|-|-|-|-|-|
        '''
        x = np.linspace(self.x1, self.x2, n+1)
        y = np.linspace(self.y1, self.y2, n+1)
        new_segments = []
        delta_n = self.delta / n
        for i in range(n):
            new_segments.append(
                Segment(x[i], y[i], x[i+1], y[i+1], length=delta_n))
        return new_segments

    def __repr__(self):
        return f'Segment({self.x1}, {self.y1}, {self.x2}, {self.y2})m'
