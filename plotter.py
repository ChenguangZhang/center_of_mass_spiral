import matplotlib.pyplot as plt


def plot_discrete_shape(discrete_shape, ax=None, **kwargs):
    if ax is None:
        fig, ax = plt.subplots()
    for segment in discrete_shape.segments:
        x = [segment.x1, segment.x2]
        y = [segment.y1, segment.y2]
        ax.plot(x, y, **kwargs)
    return ax
