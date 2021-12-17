# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 16:57:45 2021

@author: kolja
"""

import file_organizer as fo
import config_parser as cp
import numpy as np

import matplotlib.pyplot as plt

path = 'data_day_two'
file_list = fo.load_file_list(path)
selection = (fo.select_files(file_list,'meas','L'))

# print(selection)
config = [cp.load_param(path + '/' + d.filename.replace('.csv', '.txt')) for d in selection]
delays = [c.horizontal.get_time_delay() for c in config]

tau = np.array([s.tau for s in selection])

data = fo.load_files(selection)
# data = fo.df_combine(data)

# del(data['iout'])
# label = list(data.columns)
# label.remove('time')

idx = [d['signal'].idxmax() for d in data]
msig = [d.loc[i, 'signal'] for i,d in zip(idx, data)]
mtim = [d.loc[i, 'time'] for i,d in zip(idx, data)]


fig,ax = plt.subplots()
# look at index 18, 33/34, 38, 44, they dont match
i = 43
ran = slice(0,43)
for d, delay, P in zip(data[ran], delays[ran], tau[ran]):
    # d['time'] = d['time'] + delay
    d.plot(x='time', y='signal', ax=ax, label=P, color='gray')
    pass
ax.set_xlim(-0.02, 0.2)
ax.set_ylim(-0,9)

ax.scatter(mtim[ran], msig[ran])
# ax.scatter(tau[ran]*1e-3, msig[ran], marker='x')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax.legend().remove()
# print(len(label), len(delay))
# data.plot(x='time', ax=ax)
