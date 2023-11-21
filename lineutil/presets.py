
from . import style

def preset_prl():
    style.setd_serif(fontsize=16)
    style.setd_math_font()
    style.setd_subplot()
    style.setd_legend()
    style.setd_grid(color='#bbb')
    style.setd_line()
    style.setd_ticks(length=7, width=0.8)
    style.setd_minor_ticks(length=3, width=0.8)


def preset_nature():
    style.setd_sans_serif(fontsize=14)
    style.setd_regular_math_font()
    style.setd_subplot()
    style.setd_legend()
    style.setd_grid(color='#bbb')
    style.setd_line()
    style.setd_ticks(length=4, width=0.8, direction='out', double_ticks=None)
    
    