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
selection = (fo.select_files(file_list,'meas','A'))

data = fo.load_files(selection)
data = fo.df_combine(data)
data.info()
data.plot(x='time')

# fig, ax = plt.subplots()

# ref = (data[0]['time']).copy()
# for i, d in file_list.iterrows():
#     if i == 14: continue
#     print(i, d['filename'])
#     data = fo.load_sfile(d['filename'], path=path)
#     print(len(data))
#     print(data.columns)
#     fig, ax = plt.subplots()

#     data.plot(x='time', y='signal',ax=ax)
#     ax.set_ylim(0,12)
#     plt.show()
    # # try:
    #     print(i, (d.loc[0,'time']))
    # except:
        # print(i, 'Error')

# print(data[10])

