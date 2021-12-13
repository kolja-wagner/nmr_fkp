# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 18:58:42 2021

@author: kolja
"""

import matplotlib.pyplot as plt
import file_organizer as fo

# load file list
path = 'data_day_one'
file_list = fo.load_file_list(path)
selection = (fo.select_files(file_list,'meas','E'))
# load data from files
data = fo.load_files(selection)
data = fo.df_combine(data)
del(data['iout'])
data.info()

# prep data
label = list(data.columns)
label.remove('time')
P = [meas.P for meas in selection]
data['time'] = data['time'] * 1000


# show different measurements
fig,ax=plt.subplots()
ran = [0,3,5,6,7,9]
for i in ran:
    data.plot(x='time', y=label[i],ax=ax,label=P[i] )
# ax.set_xlim(-2,15)
ax.legend(title='P [ms]')
ax.set_title('T1 from Period')
ax.set_xlabel('time [ms]')
ax.set_ylabel('induced voltage [V]')

plt.show()



maximum = [data[l].max() for l in label]
