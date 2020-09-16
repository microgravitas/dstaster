from IPython.display import HTML
"""
    Inject javascript, CSS
"""

# TODO: This needs to go into dstaster.py 
display(HTML("""
<style>
h1 { margin-top: 3em !important; }
h2 { margin-top: 2em !important; }
#notebook-container { 
    width: 50% !important; 
    min-width: 800px;
    font-size: 12pt;
}

.jupyter-widgets .widget-slider {
    padding: 25px 10px;
    border: 1px solid #ced1db;
    border-radius: 2px;
    margin: 10px auto;
    background-color: #f5f6fa;
}

.jupyter-widgets label, .jupyter-widgets .widget-readout {
    font-size: 14pt;
}

.jupyter-widgets label {
    width: auto;
}b

.jupyter-widgets .widget-readout {
    background-color: #fff;
}

.hidden_code .input_area  {
    max-height: 2em;
    overflow: hidden;
}

.hidden_bar {
    text-align: center;
    padding: 2ex 0ex 2ex 15ex;
}

.hidden_bar button {
    background-color: #0077b5;
    border: 0;
    padding: 1ex 2ex .7ex 2ex;
    color: #fff;
    border-radius: 5px;
}

.hidden_bar button:hover { background-color: #ff4a6e ; }

</style>
"""))

# The following script needs to be injected as HTML, otherwise
# libraries like jQuery are not automatically available.
display(HTML("""
<script>
$(function() {
console.log('CALLED');
var cells = Jupyter.notebook.get_cells();
for(c of cells) {
    if(c._metadata['hidden']) {
        // TODO: also make sure cell is not editable
        $(c.element).addClass("hidden_code");
        
        if ($(c.element).find(".hidden_bar").length == 0) {
            $(c.element).find(".input").after(
                '<div class="hidden_bar">'+
                '<button>Show code</button>'+
                '</div>'
            )
            var hidden = true;
            $(c.element).find(".hidden_bar button")
            .click(function() {
                if(hidden) {
                    $(this).parent().parent().removeClass("hidden_code");
                    $(this).text("Hide code");
                } else {
                    $(this).parent().parent().addClass("hidden_code");
                    $(this).text("Show code");
                }
                hidden = !hidden;
            });
            
            //.text('test')
        }
    }
}
});
</script>
"""))


# Settings and visuals
import matplotlib as mpl

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
    'lightgray': '#ced1db'
}

# Colour gradient for confusion matrices. Includes white as 0 colour as means
# to keep the diagonal of the matrix uncoloured.
cmap_confusion = [(0,'#ffffff'),
        (0.0000001, colors['blue']),
        (.33, '#9c95c2'),
        (.66,colors['salmon']),
        (1,colors['salmon'])]
cmap_confusion = mpl.colors.LinearSegmentedColormap.from_list('confusion', cmap_confusion)



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
    The following is adapted from
        https://stackoverflow.com/questions/31517194/how-to-hide-one-specific-cell-input-or-output-in-ipython-notebook
"""
import random

def hide_toggle(for_next=False):
    this_cell = """$('div.cell.code_cell.rendered.selected')"""
    next_cell = this_cell + '.next()'

    toggle_text = 'Toggle show/hide'  # text shown on toggle link
    target_cell = this_cell  # target cell to control with toggle
    js_hide_current = this_cell + '.find("div.input").hide();'

    if for_next:
        target_cell = next_cell
        toggle_text += ' next cell'

    js_f_name = 'code_toggle_{}'.format(str(random.randint(1,2**64)))

    html = f"""
        <script>
            function {js_f_name}() {{
                {target_cell}.find('div.input').toggle();
            }}

            {js_hide_current}
        </script>

        <a href="javascript:{js_f_name}()">{toggle_text}</a>
    """

    return HTML(html)