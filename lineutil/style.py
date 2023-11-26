
from typing import Optional, Union

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib import ticker, colors

# rc-related

def setd_font(fontsize:int=14, fontfamily:str='sans-serif'):
    plt.rcParams['font.size'] = fontsize
    plt.rcParams['font.family'] = fontfamily


def setd_sans_serif(fontsize:int=14):
    """ Set default font to be sans-serif. Helvetica and Arial will be prefered.
    """
    plt.rcParams['font.size'] = fontsize
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Helvetica', 'Arial'] + plt.rcParams['font.sans-serif']


def setd_serif(fontsize:int=14):
    """ Set default font to be serif. Times New Roman and Times will be prefered.
    """
    plt.rcParams['font.size'] = fontsize
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman', 'Times'] + plt.rcParams['font.serif']


def setd_math_font(fontfamily:str='cm', fontstyle:str='it'):
    """ Set the mathematical font family.
    """
    plt.rc('mathtext', fontset=fontfamily, default=fontstyle)

def setd_regular_math_font():
    plt.rc('mathtext', default='regular')

def setd_subplot(linewidth:float=1, margin=0, autolimit_mode='round_numbers'):
    """ Set the default parameters for subplots.
    """
    plt.rc('axes', linewidth=linewidth, xmargin=margin, ymargin=margin, autolimit_mode=autolimit_mode)

def setd_legend(frameon:bool=False, fancybox:bool=False, framealpha:float=0):
    """ Set the default parameters for legend.
    """
    plt.rc('legend', frameon=frameon, framealpha=framealpha, fancybox=fancybox)


def setd_line(linewidth:float=1.5, markersize:float=6, edgewidth:float=0.8):
    """ Set the default parameters for lines.
    """
    plt.rc('lines', linewidth=linewidth, markersize=markersize, markeredgewidth=edgewidth)


def setd_grid(linewidth:float=0.5, color='#ccc'):
    """ Set the default parameters for grids.
    """
    plt.rc('grid', color=color, linewidth=linewidth)


def setd_ticks(axis:str='both', direction:str='in', width:float=0.5, length:float=3, double_ticks:str='both'):
    """ Set the default parameters for ticks.
    
    axis: 'x'/'y'/'both'. The axis applied to.
    double_ticks: Whether show ticks on the opposite axis.
    """
    if axis == 'both':
        groups = ('xtick', 'ytick')
    elif axis == 'x':
        groups = ('xtick',)
    elif axis == 'y':
        groups = ('ytick',)
    else:
        raise ValueError(axis)
    
    if double_ticks == 'both':
        groups2 = ('xtick', 'ytick')
    elif double_ticks == 'x':
        groups2 = ('xtick',)
    elif double_ticks == 'y':
        groups2 = ('ytick',)
    elif not double_ticks:
        groups2 = ()
    else:
        raise ValueError(double_ticks)
    
    for g in groups:
        plt.rc(g, direction=direction)
        plt.rc(g + '.major', width=width, size=length)

    for g in groups2:
        if g == 'xtick':
            plt.rc(g, top=True)
        elif g == 'ytick':
            plt.rc(g, right=True)


def setd_minor_ticks(axis='both', direction='in', width=0.5, length=2, nticks=1):
    """ Set the default parameters for ticks.
    
    axis: 'x'/'y'/'both'. The axis applied to.
    nticks: How many ticks shown between the two major ticks. (only works for matplotlib version >= 3.8)
    """
    if axis == 'both':
        groups = ('xtick', 'ytick')
    elif axis == 'x':
        groups = ('xtick',)
    elif axis == 'y':
        groups = ('ytick',)
    else:
        raise ValueError(axis)


    for g in groups:
        plt.rc(g, direction=direction)
        try:
            plt.rc(g + '.minor', width=width, size=length, visible=True, ndivs=nticks+1)
        except KeyError:
            plt.rc(g + '.minor', width=width, size=length, visible=True)

# size-related

def set_subplot_aspect(aspect:float=0.8, figure:Optional[Figure]=None):
    """ Set the aspect of all subplots.
    """
    if figure is None:
        figure = plt.gcf()

    for a in figure.get_axes():
        a.set_box_aspect(aspect)


def set_figuresize_by_subplots(alignment=None, subplot_width=5, subplot_height=4, padding_width=0, padding_height=0, scaling='qrt', figure:Optional[Figure]=None):
    """ Set figure size by assuming all subplots have the same shape.

    alignment: (nrows, ncols) or None. The alignment of subplots. Will try to determine automatically if not speicified.
    subplot_width, subplot_height: The presumed width of height of subplots.
    padding_width, padding_height: Additional paddings.
    scaling: 'linear'/'sqrt'/'qrt'. For figures with large number of subplots, the size is downscaled by (n**a) to make subplots smaller, where n is max(nrows, ncols).
        linear, sqrt, qrt specifies the power index (0, 0.5, 0.25).

    """
    if figure is None:
        figure = plt.gcf()

    if alignment is None:
        subplots = figure.get_axes()
        if not len(subplots):
            alignment = (1, 1)
        else:
            gs = subplots[0].get_gridspec()
            if gs is not None:
                alignment = (gs.nrows, gs.ncols)
            else:
                pos = [s.get_position() for s in subplots]
                xs = [(p.xmin + p.xmax)/2 for p in pos]
                ys = [(p.ymin + p.ymax)/2 for p in pos]

                def _get_nbin(l):
                    l.sort()
                    b = []
                    for l_ in l:
                        if not b or l_ - b[-1] > 0.1:
                            b.append(l_)
                    return len(b)

                alignment = (_get_nbin(ys), _get_nbin(xs))
        
    y, x = alignment
    n = max(x, y*subplot_height/subplot_width)
    if scaling == 'linear':
        s = 1
    elif scaling == 'qrt':
        s = n ** -0.25
    elif scaling == 'sqrt':
        s = n ** -0.5
    elif scaling == 'same':
        s = 1/ n
    else:
        raise ValueError(scaling)

    figure.set_size_inches(x*s * subplot_width + padding_width, y*s * subplot_height + padding_height)


def render_resized(filename:Optional[str]=None, show:Optional[bool]=None, dpi:Optional[int]=None, aspect:Optional[float]=None, transparent:bool=False,
                   figure:Optional[Figure]=None, **kwargs):
    """ Shorthand for `set_subplot_aspect()`, `set_figuresize_by_subplots()`, `plt.tight_figure()` and rendering.

    filename: str,None. The file to save. If `None` and show==`None`, will call `plt.show()`.
    show: Controls whether to show the figure. Only applies when `filename != None`.
    dpi: The figure dpi.
    aspect: The subplot aspect. Defaults to 0.6 for a single subplot, and 0.8 for other cases.

    Also when there is only a single subplot, the subfig_width defaults to 6 instead of 5.
    
    Additional arguments will be passed to `set_figuresize_by_subplots()`.
    """
    # rendering

    if figure is None:
        figure = plt.gcf()

    single_subplot = len(figure.get_axes()) == 1
    if aspect is None:
        aspect = 0.6 if single_subplot else 0.8
    
    kwargs1 = kwargs.copy()
    kwargs1.setdefault('subplot_width', 6 if single_subplot else 5)
    kwargs1.setdefault('subplot_height', kwargs1['subplot_width'] * aspect)

    set_subplot_aspect(aspect, figure)
    set_figuresize_by_subplots(**kwargs1, figure=figure)
    plt.tight_layout()

    if filename is not None:
        plt.savefig(filename, dpi=dpi, transparent=transparent)

    if filename is None or show:
        if dpi:
            figure.set_dpi(dpi)
        plt.show()


# axis formatting

def set_tick_params(axes:Optional[Axes]=None, axis:str='both', direction:str='in', width:float=0.5, length:float=3, 
                    double_ticks:str='both', **kwargs):
    """ Set the major tick formats. By default, the ticks will be inside the plot, and tick will be showing on 
        all upper/down/left/right axis.

    axes: The `Axes` instance.
    axis: 'x'/'y'/'both'.
    direction: 'in'/'out'. Whether the ticks are facing inward or outward.
    width: The linewidth of the tick.
    length: The length of the tick.
    double_ticks: 'x'/'y'/'both'. Whether showing the ticks on opposite axis (right/top).

    """

    if axes is None:
        axes = plt.gca()

    axes.tick_params(axis, which='major', direction=direction, width=width, length=length, **kwargs)

    if not double_ticks:
        return
    elif double_ticks == 'both':
        a = [axes.xaxis, axes.yaxis]
    elif double_ticks == 'x':
        a = [axes.xaxis]
    elif double_ticks == 'y':
        a = [axes.yaxis]
    else:
        raise ValueError(axis)
    
    for t in a:
        t.set_ticks_position('both')


def set_minor_tick_params(axes=None, axis:str='both', nticks:int=1, direction:str='in', width:float=0.5, length:float=2, show_ticklabel:bool=False, **kwargs):
    """ Set the minor tick formats. By default, the ticks will be inside the plot, and one minor tick will be 
        generated between two major ticks.
    """
    
    if axes is None:
        axes = plt.gca()

    if axis == 'both':
        a = [axes.xaxis, axes.yaxis]
    elif axis == 'x':
        a = [axes.xaxis]
    elif axis == 'y':
        a = [axes.yaxis]
    else:
        raise ValueError(axis)
    
    assert nticks >= 0
    
    for t in a:
        if t.get_scale() == 'log':
            t.set_minor_locator(ticker.LogLocator(subs=[10/(nticks+1)*j for j in range(1,nticks+1)]))
        else:
            t.set_minor_locator(ticker.AutoMinorLocator(nticks+1))
        if not show_ticklabel:
            t.set_minor_formatter(ticker.NullFormatter())

    axes.tick_params(axis, which='minor', direction=direction, width=width, length=length, **kwargs)
    

def set_tick_power_format(axes=None, axis:str='both', power_limit:int=5):
    """ For linear scale tick labels, mpl will display a "1e-xx" label when data is too small/big.
    This function changes the format to latex "10^xx".

    power_limit: The magnitude (greator or equal) when the offset notation is used.
    """
    if axes is None:
        axes = plt.gca()

    if axis == 'both':
        a = [axes.xaxis, axes.yaxis]
    elif axis == 'x':
        a = [axes.xaxis]
    elif axis == 'y':
        a = [axes.yaxis]
    else:
        raise ValueError(axis)
    
    for a_ in a:
        fmt = ticker.ScalarFormatter(useMathText=True)
        fmt.set_powerlimits((-power_limit, power_limit))
        a_.set_major_formatter(fmt)


def set_border(axes:Optional[Axes]=None, visible:Union[bool,str]='full', linewidth:float=1, linestyle='-', color='black'):
    """ Set border style of an axes.

    visible: True/'full'/'half'/False. The visibility. If 'half', only the left and bottom axis are visible.
    linewidth: Linewidth of the frame.
    linestyle: Linestyle of the frame.
    color: Color of the frame.
    """
    
    if axes is None:
        axes = plt.gca()

    if visible is True or visible == 'full':
        on_axis = ('top', 'bottom', 'left', 'right')
        off_axis = ()
    elif visible == 'half':
        on_axis = ('left', 'bottom')
        off_axis = ('top', 'right')
    elif not visible:
        on_axis = ()
        off_axis = ('top', 'bottom', 'left', 'right')
    else:
        raise ValueError(visible)
    
    for a in on_axis:
        axes.spines[a].set_visible(True)
        axes.spines[a].set(linewidth=linewidth, linestyle=linestyle, color=color)
    
    for a in off_axis:
        axes.spines[a].set_visible(False)
        
    if len(off_axis) == 2:
        axes.xaxis.set_ticks_position('bottom')
        axes.yaxis.set_ticks_position('left')
    elif len(off_axis) == 4:
        axes.xaxis.set_visible(False)
        axes.yaxis.set_visible(False)

def set_xylabel(xlabel, ylabel, **kwargs):
    """ Set x and y labels simutaneously.
    """
    plt.xlabel(xlabel, **kwargs)
    plt.ylabel(ylabel, **kwargs)

# widgets

def legend(*args, box:bool=False, column=None, row=None, linewidth:float=0.5, loc:str='best', axis_padding:float=0, **kwargs):
    """ A drop-in replacement for `plt.legend()`.
    
    By default, the box is not shown. If `box=True`, then (by default) will show a thin square box instead
        of mpl-style box.

    box: Whether the frame is shown;
    column: Number of columns in the legend. Alias for `ncols`.
    linewidth: Linewidth of the legend box;
    loc: Location of the legend. In addition to the default choices, 'outleft, outright, outlower outupper' are also valid for a legend out of subplot.
    axis_padding: For legends out of subplot, specify the padding distance to the subplot.
    """

    kwargs1 = kwargs.copy()
    
    kwargs1.setdefault('frameon', box)
    kwargs1.setdefault('framealpha', 0 if not box else 1)
    if column:
        kwargs1.setdefault('ncol', column)
    elif row:
        kwargs1.setdefault('ncol', round(len(plt.gca().lines)/row + 0.5))
    kwargs1.setdefault('fancybox', False)

        # handles outside
    if 'out' in loc:
        p, q = loc.split(maxsplit=1)
        box = (
            {'left':0, 'center':0.5, 'right':1, 'outleft':-axis_padding, 'outright':1+axis_padding}[q],
            {'lower':0, 'center':0.5, 'upper':1, 'outlower':-axis_padding, 'outupper':1+axis_padding}[p],
        )
        loc = {'outlower':'upper', 'outupper':'lower'}.get(p,p) + ' ' + \
            {'outleft':'right', 'outright':'left'}.get(q,q)
        
        kwargs1.setdefault('bbox_to_anchor', box)

    kwargs1['loc'] = loc
    
    l = plt.legend(*args, **kwargs1)
    if box:
        frame = l.get_frame()
        frame.set_linewidth(linewidth)
        frame.set_edgecolor('black')
    return l


def plot_subplot_labels(position:Union[str,tuple,list,dict]='upper right', formatter='(%s)', padding=(0.02, 0.02), figure:Optional[Figure]=None, **kwargs):
    """ Adding labels to subplots.

    position: 
    """
    if figure is None:
        figure = plt.gcf()

    def _translate_pos(p):
        if isinstance(p, tuple):
            return p[0], p[1], 'left', 'bottom'
        else:
            a, b = p.split(maxsplit=1)
            return {'left':padding[0], 'right':1-padding[0], 'outleft':-padding[0], 'outright':1+padding[0]}[b], \
                    {'lower':padding[1], 'upper':1-padding[1], 'outlower':-padding[1], 'outupper':1+padding[1]}[a], \
                    {'outleft':'right', 'outright':'left'}.get(b,b), \
                    {'lower':'bottom', 'upper':'top', 'outlower':'top', 'outupper':'bottom'}[a]

    if isinstance(position, (str, tuple)):
        pos = _translate_pos(position)
        mode = 0
    elif isinstance(position, list):
        pos = [_translate_pos(p) for p in position]
        mode = 1
    elif isinstance(position, dict):
        default_pos = _translate_pos(position[None])
        pos = {k:_translate_pos(v) for k,v in position.items() if k is not None}
        mode = 2
    else:
        raise ValueError(position)


    for j, a in enumerate(figure.get_axes()):
        
        if mode == 0:
            l, b, halign, valign = pos
        elif mode == 1:
            l, b, halign, valign = pos[j]
        elif mode == 2:
            l, b, halign, valign = pos.get(j+1, default_pos)
        a.text(l, b, formatter % (chr(j+97)), horizontalalignment=halign, verticalalignment=valign, transform=a.transAxes, **kwargs)

# coloring


def get_colors(name:str='default', step:Union[int, float]=0.4):
    """ Get the colors from a colormap. For continuous colormaps, will refer to step for discretization.

    step: float/int. Either the number of steps, or the step size.
    """
    from math import ceil
    cm = plt.get_cmap(name)
    if isinstance(cm, colors.LinearSegmentedColormap) or name in ('viridis', 'plasma', 'inferno', 'magma', 'cividis'):
        if isinstance(step, int):
            return [cm(x/(step-1)) for x in range(step)]
        else:
            return [cm(x*step) for x in range(ceil(1/step))]
    else:
        return cm.colors


def set_prop_cycle(axes:Optional[Axes]=None, colormap:Union[list,str]='line.default', marker_colormap:Optional[str]=None, 
                   skip_header:bool=True, combination:str='*', **kwargs):
    """ Set the property cycle of lines.

    colormap: A list of colors, or name of a colormap. Applies to lines.
    marker_colormap: Name of a colormap for points.
    skip_header: Skips the first color in the colormap. Only applies to `lineutil` custom colormaps (i.e., starting with `line.`) as it 
        defines a dark color.
    combination: '+'/'*'. Defines how the extra line styles cooprate with colors. If '*', will loop through all other properties
        before switching to the next color; If '+', will loop them at the same time.
    kwargs: {name: list_of_properties}. Additional line properties to loop. For example, `linestyle=['-','--']`.
    """
    from cycler import cycler
    
    if axes is None:
        axes = plt.gca()

    def _loop_list(l, length):
        return l * (length // len(l)) + l[:(length % len(l))]

    if isinstance(colormap, str):
        colors = get_colors(colormap)
    else:
        colors = colormap

    if skip_header and isinstance(colormap, str) and colormap.startswith('line.'):
        colors = colors[1:]

    if marker_colormap:
        marker_colors = get_colors(marker_colormap)
        if skip_header and marker_colormap.startswith('line.'):
            marker_colors = marker_colors[1:]
        color_cycler = cycler(color=colors, mfc=_loop_list(marker_colors, len(colors)))
    else:
        color_cycler = cycler(color=colors)

    if not kwargs:
        axes.set_prop_cycle(color_cycler)
    else:
        if combination == '+':
            ex_cycler = cycler(**{k: _loop_list(v, len(colors)) for k, v in kwargs.items()})
            axes.set_prop_cycle(color_cycler + ex_cycler)
        elif combination == '*':
            ex_cycler = cycler(**kwargs)
            axes.set_prop_cycle(color_cycler * ex_cycler)
        else:
            raise ValueError('Invalid combination', combination)


def skip_lineprop(axes=None):
    """ Skip the next line property in the property cycle.
    """
    if axes is None:
        axes = plt.gca()

    next(axes._get_lines.prop_cycler)


# misc

def apply_to_all_subplots(func, *args, figure:Optional[Figure]=None, **kwargs):
    """ Applies a function `func(subplot, *args, **kwargs)` to all subplots in a Figure.
    """
    if figure is None:
        figure = plt.gcf()

    for s in figure.get_axes():
        func(s, *args, **kwargs)
