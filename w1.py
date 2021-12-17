# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 12:21:31 2021

@author: kolja
"""
import matplotlib.pyplot as plt
import file_organizer as fo

from d2b import fit_t2
from scipy.signal import find_peaks


PATH = 'data_day_three'


d = fo.load_sfile('scope_173.csv', path=PATH)

fig, ax = plt.subplots()

d.plot(x='time', y='signal', ax=ax)

peaks = find_peaks(d['signal'], distance=100, height=0.6)[0]
ptime = d.loc[peaks, 'time']
pval = d.loc[peaks, 'signal']
ax.scatter(ptime, pval)



fit = fit_t2(ptime, pval, log=True)
ax.plot(ptime, fit.best_fit)
ax.set_title('MG for water-probe')
ax.text(1,2,f'T2 = {fit.params["T2"].value:.2f} $\\pm$ {fit.params["T2"].stderr:.2f}')