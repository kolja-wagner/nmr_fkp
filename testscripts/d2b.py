# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 10:32:28 2021

@author: kolja
"""


import matplotlib.pyplot as plt
import file_organizer as fo

from lmfit.models import Model
import numpy as np
from scipy.signal import find_peaks


# load file list and select
path = 'data_day_one'
file_list = fo.load_file_list(path)
# Meiboom-Gill
selection = (fo.select_files(file_list,'meas','G1'))
data1 = fo.load_files(selection)
# carr pucell
selection2 = fo.select_files(file_list, 'meas', 'G2')
data2 = fo.load_files(selection2)
data = fo.df_combine(data2+data1)


# prep data
del(data['iout'])
del(data['qout'])
# data['time'] = data['time'] * 1000
labels = list(data.columns)
labels.remove('time')
data.info()

# find peaks
peaks = [find_peaks(data[l], distance=40, height=1)[0] for l in labels]


# fit model
def fit_t2(t, y, log=False):
    def t2func(t, M0, T2, const):#
        return M0*np.exp(-t/T2)+const

    model = Model(t2func, nan_policy='omit')
    res = model.fit(y, t=t, M0=1, T2=0.02, const=0)
    if log: print(res.fit_report())
    return res

# calc fits
times = [data.loc[p,'time'] for p in peaks]
values = [data.loc[p, l] for l,p in zip(labels, peaks)]
results = [fit_t2(time, value, log=False) 
           for time,value in zip(times, values)]



# show data and peaks
fig,(ax1,ax2) = plt.subplots(2,1, figsize=(5,5), sharex=True)
ax1.set_title('Meiboom-Gill')
ax2.set_title('Carr-Purcell')

axis = [ax1,ax1,ax2,ax2]
names = ['N=30', 'N=25']*2
for l, peak, ax,n in zip(labels, peaks, axis, names):
    data.plot(x='time', y=l, ax=ax, label=n)
    ax.scatter(data['time'][peak], data[l][peak])

for ax in [ax1,ax2]:
    ax.set_xlim(-0.002,0.155)
    ax.set_ylim(0,12.5)
    ax.set_ylabel('induced current [V]')
    ax.set_xlabel('time [s]')
    ax.label_outer()
plt.show()


# show peaks and fit
fig,(ax1,ax2) = plt.subplots(2,1, figsize=(5,5), sharex=True)
ax1.set_title('Meiboom-Gill')
ax2.set_title('Carr-Purcell')

axis = [ax1,ax1,ax2,ax2]
for t, v, r, ax in zip(times, values, results, axis):
    ax.scatter(t,v)
    t2 = r.params['T2']
    ax.plot(t, r.best_fit, '--', label=f'$T_2$ = {t2.value*1000 :.2f} $\pm$ {t2.stderr*1000:.2f} ms ')
    print(r.params['T2'])
    ax.legend()
for ax in [ax1,ax2]:
    ax.set_xlim(-0.002,0.155)
    ax.set_ylim(0,12.5)
    ax.set_ylabel('induced current [V]')
    ax.set_xlabel('time [s]')
    ax.label_outer()
plt.show()

print(times)

