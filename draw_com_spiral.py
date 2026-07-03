from primitives import *
import typing

def plot_circle_spiral(theta):
    x = np.sinc(theta/np.pi)
    y = (1-np.cos(theta))/theta
    plt.plot(x, y, 'k--')

def process_shape(vertex_generator:typing.Callable, closed=True, dis_res=100, num_loop=10, name='shape'):
    vertices = vertex_generator()
    p = Polygon(vertices, closed)
    dp = p.discretize(dis_res)
    dp = dp.repeat(num_loop)
    xm, ym = dp.calculate_com_spiral()
    p.plot(color='0.5')
    plt.plot(xm, ym, color='k')
    plt.axis('equal')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(f'{name}.svg')
    plt.close()

    tm = dp.t
    np.savetxt(f'{name}.txt', np.array([tm, xm, ym]).T)
    print(f'Done with {name}')


if __name__ == '__main__':
    process_shape(lambda: VertexGenerator.parabola( 0.0, 1.0, 200,)   , False, 2,    1, 'parabola')
    process_shape(lambda: VertexGenerator.ngon    (   3, 1.0,     )   , True,  100, 10, 'ngon3')
    process_shape(lambda: VertexGenerator.ngon    (   4, 1.0,     )   , True,  100, 10, 'ngon4')
    process_shape(lambda: VertexGenerator.ngon    (   6, 1.0,     )   , True,  100, 10, 'ngon6')
    process_shape(lambda: VertexGenerator.ellipse ( 1.0, 0.5, 200,)   , True,  1,   10, 'ellipse')
    process_shape(lambda: VertexGenerator.flower  ( 1.0, 0.5, 10, 500), True,  2,   10, 'flower')
