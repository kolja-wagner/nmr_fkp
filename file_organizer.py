# -*- coding: utf-8 -*-
"""
file handeling for NRM-Versuch.
Einlesen von Oszilloskop-Messwerten.

@author: kolja
"""

import os
import csv
import pandas as pd
import numpy as np

from typing import List
from dataclasses import dataclass, fields
import warnings



@dataclass
class Meas:
    # structuring parameter
    filename: str
    path:     str
    meas:     str = None
    comment:  str = None
    useful:   bool = False
        
    # physical parameter
    F:      float = None
    A:      float = None
    B:      float = None
    N:      float = None
    tau:    float = None
    P:      float = None
    
    def __str__(self):
        return f'Meas({self.filename}, meas={self.meas}, use={self.useful})'
    

def generate_file_list(folder: str, overwrite=False)-> None:
    ''' generate initial file-list. '''
    fname = os.path.basename(folder) + '.csv'
    if os.path.exists(fname) and not overwrite:
        raise ValueError(f'{folder}: file-list exist but overwrite is set to false.')
    
    files = [{'filename': f} for i,f in enumerate(os.listdir(folder)) if '.csv' in f]
    print(f'{folder}: {len(files)} files found.')
    
    fnames = [f.name for f in fields(Meas)]
    fnames.remove('path')
    
    with open(fname, 'w', newline='\n') as f:
        writer = csv.DictWriter(f, fieldnames=fnames)
        writer.writeheader()
        writer.writerows(files)
        
def load_file_list(path: str) -> List[Meas]:
    ''' parse .csv to list[Meas].'''
    df = pd.read_csv(path+'.csv', sep=',', na_values=['Nan','X','?'], decimal=',')
    file_list = [Meas(**dict(f), path=path) for _, f in df.iterrows()]
    return file_list
            
def select_files(fileList: List[Meas], param: str, val) -> List[Meas]:
    ''' select some files from filelist.'''
    return [m for m in fileList if getattr(m, param) == val]

def parse_column_name(name:str) -> str:
    ''' Set header for scope-file-DataFrame.'''
    names = {'x-axis':'time', 
             '1':'probe',
             '2':'iout', 
             '3':'qout', 
             '4':'signal'}
    return names.get(name, name)

def load_meas(meas: Meas) -> pd.DataFrame:    
    ''' load scope-file from Meas-Objekt; returns pd.DataFrame.'''
    filename = meas.filename
    if meas.path != None:
        filename = meas.path + '/' + filename
    df = pd.read_csv(filename, skiprows=[1])
    df.columns = [parse_column_name(c) for c in df.columns]
    df.meas = meas
    
    try: 
        df.idx = int(df.meas.filename.split('.')[0].split('_')[1])
    except:
        df.idx = 0
    
    return df

def load_sfile(filename, path=None) -> pd.DataFrame:
    ''' wrapper für load_meas-function.'''
    meas = Meas(filename, path)
    return load_meas(meas)

def load_files(mlist: List[Meas]) -> List[pd.DataFrame]:
    return [load_meas(m) for m in mlist]

def df_combine(dlist: List[pd.DataFrame]):
    ref = dlist[0]
    
    # check if timescale is equal
    equal = [(ref['time'] == d['time']).all() for d in dlist]
    if not np.all(equal):
        warnings.warn("df_combine: timescales are not equal", 
                  category = UserWarning, stacklevel=2)
    
    
    for d in dlist:
        ref[f'signal_{d.idx}'] = d['signal'] 
    del(ref['signal'])
    return ref


        
    


    
def main():
    # test some functions
    # generate_file_list('data_day_two')
    import matplotlib.pyplot as plt
    
    
    path = 'data_day_two'
    all_files = load_file_list(path)
    select = select_files(all_files,'meas','K')
    print('länge:',len(all_files), len(select))
    data = load_files(select)
    ref = df_combine(data)
    
    label = list(ref.columns)
    label.remove('iout')
    label.remove('time')
     
    I = [ref[l].max() for l in label]
    P = [m.P for m in select]
    # plt.plot(P,I)
    
    
    select = select_files(all_files, 'meas', 'L')
    data = load_files(select)
    data = df_combine(data)
    del(data['iout'])
    
    fig, ax = plt.subplots()
    data.plot(x='time', ax=ax)
    ax.legend().remove()
    
    print(select[0].filename, select[10].filename, select[-1].filename)
    
    
    
    
    pass

if __name__ == '__main__':
    main()
    