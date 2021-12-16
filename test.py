# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 18:58:42 2021

@author: kolja
"""

import matplotlib.pyplot as plt
import file_organizer as fo
import pandas as pd

path = 'data_day_one'
file_list = fo.load_file_list(path)
selection = (fo.select_files(file_list,'meas','E'))

data = fo.load_files(selection)
data = fo.df_combine(data)
# data.info()

del(data['so'])
# data.plot(x='time')

# print(selection)

label = list(data.columns)
label.remove('time')
print(label)

maximum = [data[l].max() for l in label]

P = [meas.P for meas in selection]
print(P)
print(maximum)
plt.plot(P, maximum)