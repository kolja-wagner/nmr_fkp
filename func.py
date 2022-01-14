# -*- coding: utf-8 -*-
"""
Hilfsfunktionen

@author: kolja
"""

import matplotlib as mpl
from lmfit.models import Model
import numpy as np


def get_norm_cm(label: str, vmin: float, vmax: float):
    ''' get color func, colormap und norm.'''
    m = mpl.cm.get_cmap(label)
    n = mpl.colors.Normalize(vmin, vmax)
    return lambda x: m(n(x)), m, n

def fit_t2(t, y, log=False):
    def t2func(t, M0, T2, const):#
        return M0*np.exp(-t/T2)+const

    model = Model(t2func, nan_policy='omit')
    res = model.fit(y, t=t, M0=1, T2=0.02, const=0)
    if log: print(res.fit_report())
    return res


import matplotlib.ticker as ticker
import numpy as np

def ticks_minor(ax, which='x', minorCount=2):
    if which=='x':
        xtick = ax.get_xticks()
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(np.diff(xtick)[0]/minorCount))
        return
    if which=='y':
        ytick = ax.get_yticks()
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(np.diff(ytick)[0]/minorCount))
        return
    if which=='both':
        ticks_minor(ax, 'x', minorCount)
        ticks_minor(ax, 'y', minorCount)
        return
    raise ValueError("keyword 'which' has to be 'x', 'y' or 'both'")
    
def ticks_other(ax, which='x'):
    if which=='x':
        ax.tick_params(direction='in', top=True, bottom=True, which='both')
        return
    if which=='y':
        ax.tick_params(direction='in', left=True, right=True, which='both')
        return
    if which=='both':
        ticks_other(ax, 'x')
        ticks_other(ax, 'y')
        return
    raise ValueError("keyword 'which' has to be 'x', 'y' or 'both'")
        
def ticks_handle(ax, which='x', other=True, minorCount=2):
    ax.tick_params(direction='in')
    ticks_minor(ax, which, minorCount)
    if other:
        ticks_other(ax, which)
        