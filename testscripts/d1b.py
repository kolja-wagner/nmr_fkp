# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 10:06:57 2021

@author: kolja
"""

import matplotlib.pyplot as plt
import file_organizer as fo
from func import get_norm_cm
import matplotlib as mpl



path = 'data_day_one'
file_list = fo.load_file_list(path)
selection = (fo.select_files(file_list,'meas','H'))

data = fo.load_files(selection)
data = fo.df_combine(data)
data['time'] = data['time'] * 1000

# data.info()

del(data['iout'])
del(data['qout'])
# data.plot(x='time')
label = list(data.columns)
label.remove('time')

tau = [meas.tau for meas in selection]
mi = [data[l].idxmax() for l in label]
md = [data.loc[i, l] for i,l in zip(mi, label)]


ran = slice(0, 12)

fig,ax=plt.subplots()
colormap, m, n = get_norm_cm('viridis', min(tau), max(tau))
# ax2 = fig.add_axes([0.95, 0.1, 0.03, 0.8])
# cb1 = mpl.colorbar.ColorbarBase(ax=ax2, cmap=m,norm=n)
# ax2.set_ylabel('$\\tau$  [ms]')

for l, t in zip(label, tau):
    data.plot(x='time', y=l, ax=ax, label=t, color = colormap(t))
ax.scatter(data['time'][mi], md)
ax.set_xlim(-1,100)
ax.set_title('T1 from Echo')
ax.set_xlabel('time [ms]')
ax.set_ylabel('induced voltage [V]')

ax.legend(title='$\\tau$ [ms]')