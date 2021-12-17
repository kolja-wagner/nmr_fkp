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
data = fo.load_files(selection)
data = fo.df_combine(data)
del(data['iout'])
data.info()
label = list(data.columns)
label.remove('time')
P = [meas.P for meas in selection]
data['time'] = data['time'] * 1000

# show different measurements
fig,(ax,bx)=plt.subplots(1,2, sharey=True, figsize=(10,5))
# ran = [0,3,5,6,7,9]
ran = range(len(label))
for i in ran:
    data.plot(x='time', y=label[i],ax=ax,label=P[i] )
# ax.set_xlim(-2,15)
ax.legend(title='P [ms]').remove()
ax.set_xlabel('time [ms]')
ax.set_ylabel('induced voltage [V]')

# plt.show()

maximum = [data[l].max() for l in label]
period = [s.P for s in selection]
bx.scatter(period, maximum)
bx.set_xlabel('repetitionrate [ms]')
fig.suptitle('T1 from Period (dataset 1)')

plt.show()



# Neuer Versuch
path = 'data_day_two'
file_list = fo.load_file_list(path)
selection = fo.select_files(file_list, 'meas','K')
data = fo.load_files(selection)
data = fo.df_combine(data)
del(data['iout'])
data['time'] = data['time'] * 1000

label = list(data.columns)
label.remove('time')
P = [meas.P for meas in selection]
M = [data[l].max() for l in label]
fig, (ax,bx) = plt.subplots(1,2, figsize=(10,5), sharey=True)
data.plot(x='time', ax=ax)
ax.legend().remove()
ax.set_xlabel('time [ms]')
bx.scatter(P,M)
bx.set_xlabel('repetitionrate [ms]')
ax.set_ylabel('induced voltage [V]')
# bx.set_ylabel('induced voltage [V]')
fig.suptitle('T1 from Period (dataset 2)')
