# abstract class
import numpy as np
from abc import ABC, abstractmethod
from vertex_list import VertexList


class Shape(ABC):
    @abstractmethod
    def get_vertex_list(self) -> VertexList:
        pass


class NGon(Shape):
    def __init__(self, n, r):
        self.n = n
        self.r = r

    def get_vertex_list(self) -> VertexList:
        theta = np.linspace(0, 2*np.pi, self.n+1)
        xy = self.r * np.array([(np.cos(t), np.sin(t), t) for t in theta])
        return VertexList(
            name="polygon-" + str(self.n),
            vertices=xy,
            is_closed=True,
            is_discrete=False
        )


class Parabola(Shape):
    def __init__(self, xmin, xmax, num_sample):
        self.xmin = xmin
        self.xmax = xmax
        self.num_sample = num_sample

    def get_vertex_list(self) -> VertexList:
        xy = np.array([(t, t*t, t)
                      for t in np.linspace(self.xmin, self.xmax, self.num_sample)])
        return VertexList(
            name="Parabola",
            vertices=xy,
            is_closed=False,
            is_discrete=True
        )


class Ellipse(Shape):
    def __init__(self, a, b, num_sample):
        self.a = a
        self.b = b
        self.num_sample = num_sample

    def get_vertex_list(self) -> VertexList:
        theta = np.linspace(0, 2*np.pi, self.num_sample+1)
        xy = np.array([(self.a*np.cos(t), self.b*np.sin(t), t) for t in theta])
        return VertexList(
            name="Ellipse",
            vertices=xy,
            is_closed=True,
            is_discrete=False
        )


class Flower(Shape):
    def __init__(self, r=1, deltar=0.1, f=10, num_sample=100):
        self.r = r
        self.deltar = deltar
        self.f = f
        self.num_sample = num_sample

    def get_vertex_list(self) -> VertexList:
        theta = np.linspace(0, 2*np.pi, self.num_sample+1)
        xy = np.array([
            (
                (self.r + self.deltar * np.sin(self.f*t))*np.cos(t),
                (self.r + self.deltar * np.sin(self.f*t))*np.sin(t),
                t
            ) for t in theta])
        return VertexList(
            name="Flower",
            vertices=xy,
            is_closed=True,
            is_discrete=True
        )
