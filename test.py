# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 18:58:42 2021

@author: kolja
"""

import matplotlib.pyplot as plt
import file_organize as fo
import pandas as pd



file_list = fo.files_one()
# file_list.info()
result = (fo.select_files(file_list,'meas','A'))


file_list.info()
path='data_day_one'

data = [fo.load_sfile(f['filename'], path) for _,f in file_list.iterrows()]

fig, ax = plt.subplots()

ref = (data[0]['time']).copy()
for i, d in file_list.iterrows():
    if i == 14: continue
    print(i, d['filename'])
    data = fo.load_sfile(d['filename'], path=path)
    print(len(data))
    print(data.columns)
    fig, ax = plt.subplots()

    data.plot(x='time', y='signal',ax=ax)
    ax.set_ylim(0,12)
    plt.show()
    # # try:
    #     print(i, (d.loc[0,'time']))
    # except:
        # print(i, 'Error')

# print(data[10])

