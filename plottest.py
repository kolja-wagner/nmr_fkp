# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 21:46:37 2021

@author: kolja
"""

# from IPython import get_ipython
# get_ipython().run_line_magic('matplotlib', 'qt')
# get_ipython().run_line_magic('matplotlib', 'inline')


import file_organizer as fo

folder = 'data_day_one'
allFiles = fo.load_file_list(folder)

selection = fo.select_files(allFiles, 'meas','H')


data = fo.load_files(selection)

for d in data:
    print(len(d))