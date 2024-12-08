from pathlib import PosixPath
import matplotlib.pyplot as plt

import numpy as np


def create_contact_heatmap(
    groups: list[str], data: list[list[int]], title: str, heatmap_path: PosixPath, dtype=np.uint32
):
    np_data = np.array(data, dtype=dtype)

    fig, ax = plt.subplots()
    im = ax.imshow(data, cmap="magma_r")

    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("", rotation=-90, va="bottom")

    ax.set_xticks(np.arange(len(groups)), labels=groups)
    ax.set_yticks(np.arange(len(groups)), labels=groups)

    textcolors = ("black", "white")
    kw = dict(horizontalalignment="center", verticalalignment="center")
    threshold = im.norm(np_data.max()) / 2.0

    for i in range(len(groups)):
        for j in range(len(groups)):
            kw.update(color=textcolors[int(im.norm(np_data[i, j]) > threshold)])
            im.axes.text(j, i, np_data[i, j], **kw)

    ax.set_title(title)
    fig.tight_layout()

    fig.savefig(heatmap_path, bbox_inches="tight")
    plt.close(fig)
