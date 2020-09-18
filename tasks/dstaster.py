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
    line-height: 18pt;
}

/*
    Apply color scheme
*/
.edit_mode div.cell.selected::before {
    background-color: #45cc37;
}
      
.edit_mode div.cell.selected {
    border-color: #45cc37;
}
    
div.cell.selected::before,
div.cell.selected.jupyter-soft-selected::before {
    background-color: #0077b5;
}

div.input_prompt { color: #0077b5; }
div.output_prompt { color: #ff4a6e; }

/*
  Adjust widget look (only sliders for now)
*/
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
}

.jupyter-widgets .widget-readout {
    background-color: #fff;
}

/* 
    Style for 'hidden code' cells
*/
.hidden_code .input_area  {
    max-height: 4em;
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

.hidden_code .input_area {
    position: relative;
    border-bottom: 1px solid #eee;
}

.hidden_code .input_area:after {
    content: " ";
    z-index: 10;
    display: block;
    position: absolute;
    height: 100%;
    top: 0;
    left: 0;
    right: 0;
    background: rgba(255, 255, 255, .5);
    background: -webkit-linear-gradient(rgba(255, 255, 255, .5), #fff) left repeat;
    background: linear-gradient(rgba(255, 255, 255, .5), #fff) left repeat;     
}

/*
    Custom error messages (see error(...) below)
*/
.output_area .error {
    border: 2px solid #ff4a6e;
    border-radius: 5px;
    text-align: left;
}

.error .title {
    background-color: #ff4a6e;
    padding-top: 5px;
    text-indent: 1ex;
}
.error .title b { color: #fff; }
      
.error .msg {
    margin: 1ex;
}

/*
    Custom markup
*/

.note {
    font-size: 11pt;
    line-height: 12pt;
    font-style: italic;
    margin: 1ex 2ex;
}

.task .no {
    font-size: 25pt;
    line-height: 40pt;
    text-align: center;    
    color: #fff;
    flex: 0 0 35pt;    
    margin: 10pt 10pt 10pt 5pt;
    position: relative;
    z-index: 10;
}

.task .no:after {
    content: '';
    background-color: #0077b5;
    border-radius: 50%;            
    display: block;
    float: left;
    width: 35pt;
    height: 35pt;    
    margin-right: -35pt;
    position: relative;
    bottom: 0;
    z-index: -1;
}

.task .text {
    flex-grow: 1;
    align-self: center;
    padding-right: 20pt;
}

.task {
    font-size: 110%;
    line-height: 115%;
    display: flex;
    flex-wrap: nowrap;
    align-items: start;
    margin: 1em 0em 0em 0em;
}

/*
  CSS-only hints that can be revealed via :focus.
*/

.hints li { margin-bottom: 1ex; }

.hints li button {
    background-color: #727377;
    border: 0;
    padding: 2pt 8pt;
    color: #fff;
    border-radius: 5px;
}

.hints li div {
    display: none;
}

.hints li button:hover { background-color: #ff4a6e ; }
.hints li button:focus ~ div { display: block ; }

</style>
"""))

# The following script needs to be injected as HTML, otherwise
# libraries like jQuery are not automatically available.
display(HTML("""
<script>
$(function() {
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
        } else {
            // Reset state
            $(c.element).find(".hidden_bar button").text("Show code");
        }

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
    'hotpink': '#ff4a6e',
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
        (.66,colors['hotpink']),
        (1,colors['hotpink'])]
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
    Custom error messages. error(...) will display a nice css-styled
    error message and abort the current cell execution by raising a 
    (quiet) exception.
"""
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
