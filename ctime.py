# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 21:04:38 2022

@author: kolja
"""

import os.path
from datetime import datetime

import file_organizer as fo
from file_organizer import Meas 

path = "data_day_one"
file_list = fo.load_file_list(path)


def get_modifiy_time(meas: Meas, path=None) -> datetime:
    filename = meas.filename
    if path: # falls path angegeben: hinzufügen
        filename = os.path.join(path,filename)
    assert os.path.isfile(filename)
    mtime = os.path.getmtime(filename) # returns time in s since 1970
    dt = datetime.fromtimestamp(mtime) # return datetime-object
    return dt


data = list()


paths = ["data_day_one","data_day_two","data_day_three"]

for path in paths:
    file_list = fo.load_file_list(path)
    for meas in file_list:
        data.append({'filename':meas.filename, 'datetime':get_modifiy_time(meas, path=path)})

for d in data:
    print(d)
    
    
import pandas as pd
df  = pd.DataFrame(data)

df.to_csv('datetime.csv')
df.info()