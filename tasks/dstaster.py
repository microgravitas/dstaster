"""
    Note: CSS and Javscript is added through nbextension.
"""
# Settings and visuals
import matplotlib as mpl
from cycler import cycler

from ipywidgets import *
import ipywidgets as widgets

colors = {
    'blue': '#0077b5',
    'pink': '#de00a5',
    'hotpink': '#ff4a6e',
    'purple': '#8700cd',
    'green': '#45cc37',
    'yellow': '#fecb51',
    'gray': '#727377',
    'lightgray': '#ced1db'
}

color_cycler = cycler('color', [colors[n] for n in ['blue', 'pink', 'yellow', 'green', 'purple', 'hotpink']])

mpl.rcParams.update({
    "legend.fancybox": False,
    "axes.prop_cycle": color_cycler
})


# Colour gradient for confusion matrices. Includes white as 0 colour as means
# to keep the diagonal of the matrix uncoloured.
cmap_confusion = [(0,'#ffffff'),
        (0.0000001, colors['blue']),
        (.33, '#9c95c2'),
        (.66,colors['hotpink']),
        (1,colors['hotpink'])]
cmap_confusion = mpl.colors.LinearSegmentedColormap.from_list('confusion', cmap_confusion)

# Colour gradient for distances which marks the `zero distance' in green.
cmap_distance = [(0, colors['green']),
        (0.00001, colors['lightgray']),
        (0.35, colors['lightgray']),
        (.4, '#9c95c2'),
        (.5, colors['hotpink']),
        (.6, '#9c95c2'),
        (0.65, colors['lightgray']),                 
        (1, colors['lightgray'])]
cmap_distance = mpl.colors.LinearSegmentedColormap.from_list('distance', cmap_distance)

"""
    Common imports
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix

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


"""
    Custom error messages. error(...) will display a nice css-styled
    error message and abort the current cell execution by raising a
    (quiet) exception.
"""
from IPython.core.display import HTML

class StopExecution(Exception):
    def _render_traceback_(self):
        pass

def error(title, msg):
    display(HTML(f"""
        <div class="error">
            <div class="title"><b>Error:</b> {title}</div>
            <div class="msg">{msg}</div>
        </div>
    """))
    raise StopExecution
