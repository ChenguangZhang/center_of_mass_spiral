import matplotlib.pyplot as plt


def plot_polysegment(pseg, ax=None, **kwargs):
    if ax is None:
        fig, ax = plt.subplots()
    for seg in pseg:
        x = [seg.x1, seg.x2]
        y = [seg.y1, seg.y2]
        ax.plot(x, y, **kwargs)
    return ax
