import numpy as np
import matplotlib.pyplot as plt

import logging
logging.basicConfig(level=logging.INFO)

class VertexSet: # TODO factor into VertexGenerator
    def __init__(self, vertices, is_closed):
        self.vertices = vertices
        self.isclosed = is_closed

class VertexGenerator:
    @staticmethod
    def ngon(n, r):
        theta = np.linspace(0, 2*np.pi, n, endpoint=False)
        return np.array([(r*np.cos(t), r*np.sin(t), t) for t in theta])

    @staticmethod
    def parabola(xmin,xmax,num_sample):
        return np.array([(t, t*t, t) for t in np.linspace(xmin, xmax, num_sample)])

    @staticmethod
    def ellipse(a, b, num_sample):
        theta = np.linspace(0, 2*np.pi, num_sample, endpoint=False)
        return np.array([(a*np.cos(t), b*np.sin(t), t) for t in theta])

    @staticmethod
    def flower(r = 1, deltar = 0.1, f = 10, num_sample = 100):
        theta = np.linspace(0, 2*np.pi, num_sample, endpoint=False)
        return np.array([
            (
                (r + deltar * np.sin(f*t))*np.cos(t),
                (r + deltar * np.sin(f*t))*np.sin(t),
                 t
            ) for t in theta])

class DiscreteShape:
    def __init__(self, x, y, w = None, t = None):
        self.x, self.y, self.w, self.t = x, y, w, t
        if self.w is None:
            self.w = np.ones(len(self.x))

    def repeat(self, num_loop):
        if num_loop == 1:
            return DiscreteShape(self.x, self.y, self.w, self.t)

        logging.warning('The function repeat() assumes closed geometry')
        x = np.tile(self.x, num_loop)
        y = np.tile(self.y, num_loop)
        w = np.tile(self.w, num_loop)
        if self.t is None:
            logging.warning('parameter t is not provided, assuming uniform spacing around the circle')
            self.t = np.linspace(0, 2*np.pi, len(self.x))
        t = np.tile(self.t, num_loop)
        for i in range(1, num_loop):
            t[i*len(self.t):(i+1)*len(self.t)] += i*2*np.pi
        return DiscreteShape(x, y, w, t)

    def calculate_com_spiral(self):
        mass = np.cumsum(self.w)
        mass_x = np.cumsum(self.w*self.x) / mass
        mass_y = np.cumsum(self.w*self.y) / mass
        return mass_x, mass_y
    

class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def length(self):
        return np.sqrt((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2)

    def plot(self):
        plt.plot([self.x1, self.x2], [self.y1, self.y2], 'k-')

    def discretize(self, n):
        '''
        Subdivide one segment into n uniform segments. For example
        |---------------------------| =>
        |-*-|-*-|-*-|-*-|-*-|-*-|-*-|, where * is the midpoint of each segment
        '''
        x = np.linspace(self.x1, self.x2, n+1)
        y = np.linspace(self.y1, self.y2, n+1)
        xmid = (x[1:] + x[:-1]) / 2
        ymid = (y[1:] + y[:-1]) / 2
        wmid = self.length() / (n * np.ones(n))
        return np.array(xmid), np.array(ymid), np.array(wmid)

    def __repr__(self):
        return f'Segment({self.x1}, {self.y1}, {self.x2}, {self.y2})m'

class Polygon:
    def __init__(self, vertices, closed = True):
        self.vertices = vertices
        self.is_parametric = (len(vertices[0]) == 3)
        self.is_closed = closed
        if self.is_closed:
            assert len(self.vertices) > 2, 'A closed polygon should have at least 3 vertices'
            logging.info('Close the polygon')
            # close the polygon by extending the numpy array
            self.vertices = np.vstack((self.vertices, self.vertices[0]))
            logging.info(f'Closed polygon has {len(self.vertices)} vertices')
            if self.is_parametric:
                # linearly extrapolate the angle for the last vertex
                t_m1 = self.vertices[-2][2]
                t_m2 = self.vertices[-3][2]
                self.vertices[-1][2] = 2*t_m1 - t_m2
        self.num_vertices = len(self.vertices)

    def plot(self, *args, **kwargs):
        for i in range(self.num_vertices-1):
            x1, y1 = self.vertices[i][:2]
            x2, y2 = self.vertices[i+1][:2]
            plt.plot([x1, x2], [y1, y2], *args, **kwargs)

    def discretize(self, n):
        x, y, w, t = [], [], [], []
        for i in range(self.num_vertices-1):
            x1, y1 = self.vertices[i][:2]
            x2, y2 = self.vertices[i+1][:2]
            s = Line(x1, y1, x2, y2)
            xmid, ymid, lmid = s.discretize(n)
            x.extend(xmid)
            y.extend(ymid)
            w.extend(lmid)

            if self.is_parametric:
                t1 = self.vertices[i][2]
                t2 = self.vertices[i+1][2]
                t_ = np.linspace(t1, t2, n+1)
                tmid = (t_[1:] + t_[:-1]) / 2
                t.extend(tmid)

        return DiscreteShape(np.array(x), np.array(y), np.array(w), np.array(t))

    def __repr__(self):
        return f'Polygon({self.vertices})'
