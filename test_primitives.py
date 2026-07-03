from primitives import *

def test_Line():
    s = Line(0, 0, 1, 1)
    print(s)
    print(s.length())
    x, y, w = s.generate_uniform_segments(5)
    plt.plot(x, y, 'ro')
    s.plot()
    plt.show()

def test_Polygon():
    n = 6
    r = 1
    polygon_verticies = VertexGenerator.ngon(n, r)
    p = Polygon(polygon_verticies)
    p.plot()
    x, y, w, t = p.generate_uniform_segments(5)
    plt.plot(x, y, 'ro')
    plt.show()