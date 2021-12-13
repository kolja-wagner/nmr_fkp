# -*- coding: utf-8 -*-
"""
Hilfsfunktionen

@author: kolja
"""

import matplotlib as mpl


def get_norm_cm(label: str, vmin: float, vmax: float):
    ''' get color func, colormap und norm.'''
    m = mpl.cm.get_cmap(label)
    n = mpl.colors.Normalize(vmin, vmax)
    return lambda x: m(n(x)), m, n

