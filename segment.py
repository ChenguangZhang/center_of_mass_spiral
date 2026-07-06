import numpy as np


class Segment:
    def __init__(self, x1, y1, x2, y2, length=None):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        if length is not None:
            self.length = length
        else:
            self.length = self.__length()

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
        lsub = self.length / n
        for i in range(n):
            new_segments.append(
                Segment(x[i], y[i], x[i+1], y[i+1], length=lsub))
        return new_segments

    def __repr__(self):
        return f'Segment({self.x1}, {self.y1}, {self.x2}, {self.y2})m'
