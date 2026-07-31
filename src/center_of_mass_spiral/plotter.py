import matplotlib.pyplot as plt
import numpy as np
from .poly_segment import PolySegment


def plot_polysegment(pseg: PolySegment, ax=None, **kwargs):
    if ax is None:
        fig, ax = plt.subplots()
    vl = pseg.vertex_list
    if vl.num_repeat == 1:
        V = vl.vertices
    else:
        n_first_loop = (len(vl.vertices) - 1) // vl.num_repeat + 1
        V = vl.vertices[:n_first_loop, :]

    ax.plot(V[:, 0], V[:, 1], **kwargs)
    return ax
