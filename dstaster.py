import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from sklearn.metrics import confusion_matrix

# Settings
mpl.rcParams.update({
    "legend.fancybox": False
})

colors = {
    'blue': '#0077b5',
    'pink': '#de00a5',
    'salmon': '#ff4a6e',
    'purple': '#8700cd',
    'green': '#45cc37',
    'yellow': '#fecb51',
    'gray': '#727377',
    'lightgray': '#ced1db',
    'lightestgray': '#f5f6fa'
}

# Colour gradient for confusion matrices. Includes white as 0 colour as means
# to keep the diagonal of the matrix uncoloured.
cmap_confusion = [(0,'#ffffff'),
        (0.0000001, colors['blue']),
        (.33, '#9c95c2'),
        (.66,colors['salmon']),
        (1,colors['salmon'])]
cmap_confusion = mpl.colors.LinearSegmentedColormap.from_list('confusion', cmap_confusion)


def plot_confusion_matrix(truth, pred, labels, ax, cmap=None):
    labels = list(labels) # In case it's an iterator
    C = confusion_matrix(truth, pred, labels=labels, normalize='true')

    if not cmap:
        cmap = cmap_confusion

    CC = C.copy()
    k = len(labels)
    CC[np.eye(k,k) == 1] = 0

    ax.imshow(CC, cmap=cmap, vmin=0, vmax=1)

    for i in range(k):
        p = C[i,i]
        col = cmap((1-p))
        text = ax.text(i, i, "{:.1f}%".format(C[i, i]*100),
                   ha="center", va="center", weight='bold', fontsize=14, color=col)

    for i in range(k):
        for j in range(k):
            if i == j:
                continue
            p = C[j,i]
            text = ax.text(i, j, "{:.1f}%".format(p*100),
                       ha="center", va="center", color='white', fontsize=12)

    # labels, title and ticks
    ax.set_xlabel('Predicted label');
    ax.set_ylabel('True label');
    ax.xaxis.set_ticks(range(k))
    ax.xaxis.set_ticklabels(labels);
    ax.yaxis.set_ticks(range(k))
    ax.yaxis.set_ticklabels(labels)

    # Hide spines and tick lines
    for s in ax.spines:
        ax.spines[s].set_visible(False)
    ax.tick_params(axis='both', which='both', length=0, pad=7)
