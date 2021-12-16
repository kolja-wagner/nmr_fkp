# -*- coding: utf-8 -*-
"""
PASER FÜR OSZILLOSKOP-CONFIG-DATEN

@author: kolja
"""

import os
import datetime
from dataclasses import dataclass    
from typing import List, Dict

_KEYWORDS = ['ANALOG', 'TRIGGER', 'HORIZONTAL', 'ACQUISITION', 'MEASUREMENTS']

@dataclass
class Channel:
    ch: str
    scale: str
    pos: str
    coup: str
    bw_limit: str
    inv: str
    imp: str
    probe: str
    skew: str 
    
    @classmethod
    def from_info(cls, info: str):
        ch_list = [c.strip().split(' ') for c in info]
        for i,c in enumerate(ch_list):
            if c[0] =='Ch':
                ch_list.append(c[2:])
                ch_list[i] = c[:2]
            elif c[0] == 'BW':
                ch_list[i] = ['bw_limit', c[-1]]
            else:
                ch_list[i] = [c[0], ''.join(c[1:])]
        ch_dict = {c[0].lower():c[1] for c in ch_list}
        return Channel(**ch_dict)

@dataclass
class Trigger:
    sweep: str
    coup: str
    noise_rej: str
    hf_rej: str
    holdoff: str
    mode: str
    source: str
    slope: str
    level: str
    
    @classmethod
    def from_info(cls, info: str):
        elements = [s.strip().split(' ') for s in ','.join(info.split('\n')).split(',')]
        for i, e in enumerate(elements):
            if e[0] == 'Sweep':
                elements[i] = ['sweep', e[2]]
            if e[0] == 'Noise':
                elements[i] = ['noise_rej', e[2]]
            if e[0] == 'HF':
                elements[i] = ['hf_rej', e[2]]
        e_dict = {e[0].lower() : e[1] for e in elements}
        return Trigger(**e_dict)
        
@dataclass
class Horizontal:
    mode: str
    ref: str
    scale: str
    delay: str
    
    @classmethod
    def from_info(cls, info: str):
        info = [i.strip() for i in info.split(',')]
        info = [i.replace('Main ', '') for i in info]
        info = {k.split(' ')[0].lower():k.split(' ')[1] for k in info}
        return Horizontal(**info)

@dataclass
class Acquisition:
    mode: str
    realtime: str
    vectors: str
    persistence: str
    
    @classmethod
    def from_info(cls, info: str):
        elements = [s.strip().split(' ') for s in info.split(',')]
        e_dict = {e[0].lower():e[1] for e in elements}
        return Acquisition(**e_dict) 
    
@dataclass
class Measurements:
    info:str
    
    @classmethod
    def from_info(cls, info: str):
        return Measurements(info)

@dataclass
class OszParam:
    file: str
    datetime: datetime.datetime
    analog: list[Channel]
    horizontal: Horizontal
    trigger: Trigger
    acquisition: Acquisition
    measurements: Measurements
        
    
def _read_file(path: str) -> List[str]:
    ''' read file and search for keywords. '''
    with open(path, mode='r') as f:
        lines = f.readlines()    
        idx = dict()
        for i,l in enumerate(lines):
            idx.update({k:i for k in _KEYWORDS if k in l})
    return lines
    
def _get_indices(lines: List[str]) -> Dict[str,int]:
    ''' get line indices for keywords. '''
    idx = dict()
    for i, l in enumerate(lines):
        idx.update({k:i for k in _KEYWORDS if k in l})
    return idx

def _info_from_keyword(k: str, idx: int, lines: List[str]) -> str:
    '''return text for each keywords.'''
    indices = list(idx.values()) + [len(lines)]
    i = _KEYWORDS.index(k)
    j = _KEYWORDS.index(k)+1
    info = ''.join(lines[indices[i]+1:indices[j]]).strip()
    return info
        
def _parse_info(k: str, info: str):
    '''parse infostrign to dataclass.'''
    
    if k == 'ANALOG':
        lines = info.split('\n')
        n_channels = int(len(lines)/2)
        channels = [','.join(lines[2*i:2*i+2]).split(',') for i in range(n_channels)]
        return [Channel.from_info(c) for c in channels]
    elif k == 'TRIGGER':
        return Trigger.from_info(info)
    elif k == 'HORIZONTAL':
        return Horizontal.from_info(info)
    elif k == 'ACQUISITION':
        return Acquisition.from_info(info)
    elif k == 'MEASUREMENTS':
        return Measurements.from_info(info)
    else:
        raise ValueError(f'Key "{k}" not found')
    
def load_param(path):
    '''Parse Oszilloskop-Config main function of modul.'''
    lines = _read_file(path)
    idx = _get_indices(lines)
    time = os.path.getctime(path)
    dtime = datetime.datetime.fromtimestamp(time)

    r_dict = {'file': path, 'datetime': dtime}
    for k in _KEYWORDS:        
        info = _info_from_keyword(k, idx, lines)
        kval = _parse_info(k, info)
        r_dict[k.lower()] = kval
        
    return OszParam(**r_dict)
    


def _test():
    path = r'data_day_two/scope_140.txt'
    lines = _read_file(path)
    idx = _get_indices(lines)
    
    k = 'HORIZONTAL'
    for k in _KEYWORDS:
        info = _info_from_keyword(k, idx, lines)
        print(_parse_info(k, info), '\n')
        
    p = load_param(path)
    print(p)


if __name__ == '__main__' :
    _test()        