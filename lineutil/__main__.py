
# -x [] -y [] --lw

import argparse
import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
import os.path
from . import colormap
from . import style

def parse_cols1(x, data):
    try:
        v = int(x)
    except ValueError:
        xcol = data.loc[:, x]
        xtitle = x
    else:
        if v == 0:
            xcol = data.index
        else:
            xcol = data.iloc[:, v-1]
            xtitle = data.columns[v-1]

    return xcol, xtitle

def parse_cols(x:str, y:str, data:pd.DataFrame):
    # x: a single number or string
    # y: x or number:number or x,x,...x
    # returns x, ys, xtitle, ytitles
    
    xcol, xtitle = parse_cols1(x, data)
    
    if ':' in y:
        start, end = y.split(':')
        vstart = 0 if start == '' else int(start)-1
        vend = data.shape[1] if end == '' else int(end)-1
        ycol = data.iloc[:, vstart:vend]
        ytitle = [x for x in data.columns[vstart:vend]]

    else:
        cols = []
        titles = []
        for y_ in y.split(','):
            ycol_, ytitle_ = parse_cols1(y_, data)
            cols.append(ycol_)
            titles.append(ytitle_)

        ycol = pd.DataFrame(dict(zip(titles, cols)))
        ytitle = titles

    return xcol, ycol, xtitle, ytitle
        

def parse_token(token:str):
    """ Parse string into one of int,float,bool,None,str.
    """
    try:
        return {'true':True, 'false':False}[token.lower()]
    except KeyError:
        pass
    if token.lower() == 'none':
        return None
    
    if '.' in token or 'e' in token:
        try:
            return float(token)
        except ValueError:
            return token
    try:
        return int(token)
    except ValueError:
        return token

def parse_dict(s, translation):
    if s is None or s == '':
        return {}
    else:
        r = {}
        for ss in s.split(','):
            p, q = ss.split('=', 1)
            r[translation.get(p, p)] = parse_token(q)
        return r

def parse_range(s):
    p, q = s.split(':', 1)
    return (float(p) if p else None, float(q) if q else None)

def parse_bool(s):
    return {'true':True, 'false':False}[s.lower()]


def main():

    parser = argparse.ArgumentParser('plot one or multiple files')
    parser.add_argument('-x', default='1', help='The identifier of x column. Either a number (starting from 1) or a column title')
    parser.add_argument('-y', default='2:', help='The identifier of y columns. One of a number, a column title or a range (like "1:5")')
    parser.add_argument('-s', '--style', action='append', nargs='?', help='Keyword arguments passed to individual plt.plot() call respectively, with format "key=args,key2=arg2,..."')
    parser.add_argument('-cm', '--colormap', action='append', nargs='?', help='Name of the colormap')
    parser.add_argument('-mcm', '--markercolormap', default='lighter', help='Name of the colormap for the marker facecolor; OR one of "same"/"lighter" ')
    parser.add_argument('--default', help='Keyword arguments passed to all plt.plot() calls. In the format "key=args,key2=arg2,..."')
    parser.add_argument('--header', type=parse_bool, default=True, help='Whether file has a header of column names')
    parser.add_argument('--sep', default='\s+', help='Separator of the input file')
    # parser.add_argument('--overlay', choices=['direct', 'subplot'], default='direct') # direct/subplot/figure
    parser.add_argument('--save', help='Filename (if save)')
    parser.add_argument('--xlabel', help='Label of x axis')
    parser.add_argument('--ylabel', help='Label of y axis')
    parser.add_argument('--xlim', help='Range of x in the format "start:end"')
    parser.add_argument('--ylim', help='Range of y in the format "start:end"')
    parser.add_argument('--log', choices=['x','y','all'], help='Use log plotting')
    parser.add_argument('--dpi', type=int, help='DPI')
    parser.add_argument('--aspect', type=float, help='Aspect of the subplots')
    parser.add_argument('--title', help='Title of the figure')
    parser.add_argument('--legend', help='Legend and legend arguments', type=str, default='True')
    parser.add_argument('files', nargs='+')

    args = parser.parse_args()

    translation = {'c':'color', 'lc':'color', 'lt':'linestyle', 'pt':'marker', 'ps':'markersize', 
                   'fill':'fillstyle', 'edgecolor':'markeredgecolor', 'facecolor':'markerfacecolor'}

    default_style = parse_dict(args.default, translation)
    header = None if not args.header else 0
    if args.style is None:
        args.style = []
    
    styles = []
    for j in range(len(args.files)):
        if j < len(args.style):
            d = default_style.copy()
            d.update(parse_dict(args.style[j], translation))
            styles.append(d)
        else:
            styles.append(default_style)

    try:
        legend = parse_bool(args.legend)
        legend_style = {}
    except KeyError:
        legend = True
        legend_style = parse_dict(args.legend, translation)

    style.setd_sans_serif()
    style.setd_legend()
    style.setd_line()
    style.setd_ticks()
    style.setd_subplot(linewidth=0.8)
    style.setd_minor_ticks()

    plt.figure('line')

    if len(args.files) == 1:
        fileprefix = ['']
    else:
        if len(set((os.path.basename(x) for x in args.files))) == len(args.files):
            fileprefix = [os.path.basename(x) + ':' for x in args.files]
        else:
            fileprefix = [x + ':' for x in args.files]

    if args.colormap is None:
        colormaps = ['line.default'] * len(args.files)
    else:
        colormaps = [x if x else 'line.default' for x in args.colormap]
        colormaps += [colormaps[-1]] * (len(args.files) - len(colormaps))

    xtitles = set()
    ytitles = set()
    for n, file in enumerate(args.files):
        data = pd.read_csv(file, sep=args.sep, header=header, index_col=False)
        xcol, ycol, xtitle, ytitle = parse_cols(args.x, args.y, data)


        # marker color: If styles is empty, need to inject to colormap
        # else -- inject to styles
        if args.markercolormap == 'same':
            if 'color' in styles[n]:
                styles[n].setdefault('markerfacecolor', styles[n]['color'])
                marker_colormap = None
            else:
                marker_colormap = colormaps[n]
        elif args.markercolormap == 'lighter':
            if 'color' in styles[n]:
                styles[n].setdefault('markerfacecolor', style.lighten_color(*style.name2color(styles[n]['color'])))
                marker_colormap = None
            else:
                if colormaps[n] == 'line.default':
                    marker_colormap = 'line.lighter'
                else:
                    marker_colormap = [style.lighten_color(*c[:3]) for c in style.get_colors(colormaps[n])]
        else:
            marker_colormap = args.markercolormap

        style.set_prop_cycle(colormap=colormaps[n], marker_colormap=marker_colormap)

        for j in range(ycol.shape[1]):
            plotfunc = {None:plt.plot, 'x':plt.semilogx, 'y':plt.semilogy, 'all':plt.loglog}[args.log]
            plotfunc(xcol, ycol.iloc[:,j], label=fileprefix[n] + ytitle[j], **styles[n])

        xtitles.add(xtitle)
        if len(ytitle) == 1:
            ytitles.add(ytitle[0])

    if args.xlim:
        plt.xlim(parse_range(args.xlim))
    if args.ylim:
        plt.ylim(parse_range(args.ylim))


    if args.xlabel is None and len(xtitles) == 1:
        plt.xlabel(xtitles.pop())
    elif args.xlabel is not None:
        plt.xlabel(args.xlabel)

    if args.ylabel is None and ytitles and len(ytitles) == 1:
        plt.ylabel(ytitles.pop())
    elif args.ylabel is not None:
        plt.ylabel(args.ylabel)

    if args.title:
        plt.title(args.title)

    if legend:
        style.legend(**legend_style)

    style.render_resized(filename=args.save, dpi=args.dpi, aspect=args.aspect) 
    

if __name__ == '__main__':
    main()
