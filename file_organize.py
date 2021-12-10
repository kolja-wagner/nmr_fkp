# -*- coding: utf-8 -*-
"""
File handeling

@author: kolja
"""

import os
import csv
import pandas as pd

PATH = ''

def get_list_of_files(folder: str, overwrite=False):
    fname = os.path.basename(folder) + '.csv'
    if os.path.exists(fname) and not overwrite:
        raise ValueError(f'{folder}: file-list exist but overwrite is set to false.')
    
    files = [{'filename': f, 'n':i} for i,f in enumerate(os.listdir(folder)) if '.csv' in f]
    # files = [f.update('i',i) for i,f in enumerate(files)]
    print(f'{folder}: {len(files)} files found.')
    
    with open(fname, 'w', newline='\n') as f:
        writer = csv.DictWriter(f, fieldnames=['n','filename', 'meas','comment'])
        writer.writeheader()
        writer.writerows(files)
        
def files_one():
    df= pd.read_csv('data_day_one.csv', sep=';')
    return df

def main():
    # folder = 'data_day_one'    
    # get_list_of_files(folder, overwrite=False)
    files_one()
    pass
if __name__ == '__main__':
    main()
    