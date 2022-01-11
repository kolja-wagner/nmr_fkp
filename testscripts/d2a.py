# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 10:14:13 2021

@author: kolja
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np


from d2b import fit_t2
import file_organizer as fo

# import file list and select files
path = 'data_day_one'
file_list = fo.load_file_list(path)
selection = (fo.select_files(file_list,'meas','F'))

# load data to pd.dataFrame
data = fo.load_files(selection)
data = fo.df_combine(data)
# data.info()
del(data['iout'])
del(data['qout'])

# extract parameter (label, tau)
label = list(data.columns)
label.remove('time')
tau = np.array([meas.tau for meas in selection])*1000 


# peak-finding
peaks = [find_peaks(data[l], height=2, distance=40, width=10)[0] for l in label]
idx = [peaks[0][0]] + [p[1] for p in peaks[1:]]
times = data['time'][idx]
values = np.array([data.loc[i, l] for i,l in zip(idx, label)])

# use fit-function from another file
result = fit_t2(times[1:], values[1:], log=True)
t2 = result.params['T2']


fig,ax=plt.subplots()
ran = slice(0, 20,1) # reduce lines
# fancy-color-nonsens
from func import get_norm_cm
colormap, m, n = get_norm_cm('viridis', min(tau), max(tau))
ax2 = fig.add_axes([0.95, 0.1, 0.03, 0.8])
cb1 = mpl.colorbar.ColorbarBase(ax=ax2, cmap=m,norm=n)
ax2.set_ylabel('$\\tau$ [ms]')

# plot data
for l, t, in zip(label[ran], tau[ran]):
    data.plot(x='time', y=l, ax=ax, label='', color=colormap(t))
ax.plot([],[], label='Measurements', color='black')
ax.scatter(times, values, label='Peaks')
ax.plot(times[1:], result.best_fit, '--', label=f'Exponential-Fit:\n$T_2$ = {t2.value*1000 :.2f} $\pm$ {t2.stderr*1000:.2f} ms ')


ax.legend().remove()
ax.set_xlabel('time [s]')
ax.set_ylabel('induced voltage [V]')
ax.set_xlim(-0.002,0.1)
ax.set_title('T2 from Hahn-echo (multiple measurements)')
ax.legend()
plt.show()




