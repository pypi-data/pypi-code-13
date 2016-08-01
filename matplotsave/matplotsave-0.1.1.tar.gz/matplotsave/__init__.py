import contextlib
import matplotlib.pyplot as plt


@contextlib.contextmanager
def plot_and_save(filename, *, title=None, xlabel=None, ylabel=None, shape=(1, 1), size=None, dpi=None):
    fig = plt.figure(figsize=size)
    ax = fig.add_subplot(*(shape + (1,)))
    if not title is None:
        ax.set_title(title)
    if not xlabel is None:
        ax.set_xlabel(xlabel)
    if not ylabel is None:
        ax.set_ylabel(ylabel)
    yield (fig, ax)
    fig.savefig(filename, dpi=dpi)
    fig.clear()
