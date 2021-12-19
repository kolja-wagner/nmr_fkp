# -*- coding: utf-8 -*-
"""
Created on Sun Dec 19 16:48:57 2021

@author: kolja
"""

import matplotlib.pyplot as plt
import file_organizer as fo

from d2b import fit_t2
from scipy.signal import find_peaks

PATH = 'data_day_three'
# fo.generate_file_list(PATH)

liste = fo.load_file_list(PATH)
print(liste)

for i in range(len(liste)):
    d = fo.load_sfile(liste[i].filename, path=PATH)

    d.plot(x='time', y='signal')