# -*- coding: utf-8 -*-
"""
file handeling for NRM-Versuch

@author: kolja
"""

import os
import csv
import pandas as pd
import numpy as np

from dataclasses import dataclass

@dataclass
class Meas:
    # structuring parameter
    filename: str
    path:     str
    meas:     str = None
    comment:  str = None
    useful:   bool = False
        
    # physical parameter
    F:          float = None
    A_len:      float = None
    B_len:      float = None
    B_count:    float = None
    tau:        float = None
    P:          float = None
    
    def __str__(self):
        return f'Meas({self.filename}, meas={self.meas}, use={self.useful})'
    

def generate_file_list(folder: str, overwrite=False)-> None:
    ''' generate initial file-list. '''
    fname = os.path.basename(folder) + '.csv'
    if os.path.exists(fname) and not overwrite:
        raise ValueError(f'{folder}: file-list exist but overwrite is set to false.')
    
    files = [{'filename': f, 'n':i} for i,f in enumerate(os.listdir(folder)) if '.csv' in f]
    print(f'{folder}: {len(files)} files found.')
    
    with open(fname, 'w', newline='\n') as f:
        writer = csv.DictWriter(f, fieldnames=['n','filename', 'meas'])
        writer.writeheader()
        writer.writerows(files)
        
def load_file_list(path: str) -> list[Meas]:
    ''' parse .csv to list[Meas].'''
    df = pd.read_csv(path+'.csv', sep=',', na_values=['Nan','X','?'], decimal=',')
    file_list = [Meas(**dict(f), path=path) for _, f in df.iterrows()]
    return file_list
            
def select_files(fileList: list[Meas], param: str, val) -> list[Meas]:
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

def load_files(mlist: list[Meas]) -> list[pd.DataFrame]:
    return [load_meas(m) for m in mlist]

def df_combine(dlist: list[pd.DataFrame]):
    ref = dlist[0]
    equal = [(ref['time'] == d['time']).all() for d in dlist]
    # print('equal: ', np.all(equal))
    
    for d in dlist:
        ref[f'signal_{d.idx}'] = d['signal'] 
    del(ref['signal'])
    return ref


        
    


    
def main():
    # test some functions
    
    path = 'data_day_one'
    all_files = load_file_list(path)
    select = select_files(all_files,'meas','H')
    
    print('länge:',len(all_files), len(select))
    # data = load_files(select)
    # print(data[0].meas)
    
    print(select[0].tau)
    # ref = data[0]
    # print('equal: ', )
    
    # ref = df_combine(data)
    # print(ref.idx)
    
    # equal = [ (ref['time'] == d['time']).all() for d in data]
    # print('equal:', np.all(equal))
    
    # for d in data:
    #     d.idx = int(d.meas.filename.split('.')[0].split('_')[1])
    #     equal = (ref['time'] == d['time']).all()
    #     print(d.idx, equal)
        
    #     ref[f'signal_{d.idx}'] = d['signal'] 
    # del(ref['signal'])
    # ref.info()
    
    # ref.plot(x='time')
    
    
    pass

if __name__ == '__main__':
    main()
    