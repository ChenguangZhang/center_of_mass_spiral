import matplotlib.pyplot as plt
import numpy as np
from .poly_segment import PolySegment


# from .perf_tools import timing_decorator
# @timing_decorator # disabled after profiling
def plot_polysegment(pseg: PolySegment, ax=None, **kwargs):
    if ax is None:
        fig, ax = plt.subplots()
    vl = pseg.vertex_list
    if vl.num_repeat == 1:
        V = vl.vertices
    else:
        # Math is a bit tricky here. Consider a square. It is defined by 5 vertices
        # (the first and last overlap). When repeating, we drop the last vertex,
        # repeat, and add it back.
        # For example, after repeating 3 times, the number of vertices is
        #                              (5-1)*3+1=13.
        # To recover the vertex count in the first loop, we need to reverse the above formula:
        #                         (len(vl) - 1)/n_repeat + 1.
        # which is the one used below.
        n_first_loop = (len(vl.vertices) - 1) // vl.num_repeat + 1
        V = vl.vertices[:n_first_loop, :]

    ax.plot(V[:, 0], V[:, 1], **kwargs)
    return ax
