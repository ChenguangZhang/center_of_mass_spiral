import matplotlib.pyplot as plt


def plot_polysegment(pseg, ax=None, **kwargs):
    if ax is None:
        fig, ax = plt.subplots()
    for segment in pseg:
        x = [segment.x1, segment.x2]
        y = [segment.y1, segment.y2]
        ax.plot(x, y, **kwargs)
    return ax
