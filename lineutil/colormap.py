_colors = {
    "default": [
        "#000000", "#e61919", "#1e77e5", "#33a02b", "#ff8000", "#7e46b9", "#ff1ab3", "#b8752e", "#d8d80a", "#ff7f7f", "#efbaa3", "#99ccff", "#7fe2a3", "#ffcc00", "#cc99ff"
    ],
    "lighter": [
        "#b3b3b3", "#ff6666", "#99ccff", "#7fe2a3", "#ffcc00", "#cc99ff", "#ff99cc", "#f7b56e", "#ffff4d", "#ffb3b3", "#f3e6be"
    ],
    "lighter+": [
        "#bfbfbf", "#fad1d1", "#d1e3fa", "#c6efc3", "#fce6cf", "#e5daf1", "#fccfe6"
    ],
    "lighter++": [
        "#f2f2f2", "#fce8e8", "#e8f1fc", "#ecfaeb", "#fdf3e7", "#f2edf8", "#fde7f3"
    ],
    "darker": [
        "#000000", "#983a1b", "#1b5398", "#267920", "#aa5909", "#583281", "#8a0f4d"
    ],
    "contrast1": [
        "#000000", "#e21919", "#00008c", "#39ac58", "#dfa920", "#cc66cc"
    ],
    "vivid": [
        "#a8a8a8", "#ff2300", "#008cf2", "#6bd69b", "#ffd675", "#9335ff", "#ff9300"
    ],
    "pair" :[
        "#000000", "#e61919", "#ffa299", "#1e77e5", "#99ccff", "#33a02b", "#7fe2a3", "#ff8000", "#ffd480", "#7e46b9", "#cc99ff"
    ],
    "gdv": [
        "#000000", "#ff1f5b", "#00cd6c", "#009ade", "#af58ba", "#ffc61e", "#f28522", "#a0b1ba", "#a6761d"
    ],
    "gdv3": [
        "#000000", "#e9002d", "#ffaa00", "#00b000"
    ],
    "cool3": [
        "#000000", "#ff33bb", "#4d88ff", "#ff4000",
    ],
    "cold3": [
        "#000000", "#00c261", "#4d88ff", "#b366ff",
    ]
}

from matplotlib.colors import ListedColormap, to_rgb
import matplotlib

def _load_colormaps():

    for name, cl in _colors.items():
        matplotlib.colormaps.register(ListedColormap([to_rgb(c) for c in cl], 'line.' + name))

_load_colormaps()
