# -*- coding: utf-8 -*-
"""
PASER FÜR OSZILLOSKOP-CONFIG-DATEN

@author: kolja
"""

import os
import datetime
from dataclasses import dataclass    
from deprecated import deprecated
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
                ch_list[i] = ['ch', int(c[1])]
            elif c[0] == 'BW':
                ch_list[i] = ['bw_limit', c[-1]]
            else:
                ch_list[i] = [c[0], ''.join(c[1:])]
        ch_dict = {c[0].lower():c[1] for c in ch_list}
        for k,v in ch_dict.items():
            if isinstance(v, str) and v.lower() == "on":
                ch_dict[k] = True
            if isinstance(v, str) and v.lower() == "off":
                ch_dict[k] = False
        
        return Channel(**ch_dict)

    def get_voffset(self):
        if 'mV' in self.pos:
            return float(self.pos[:-2])*1e-3
        elif 'V' in self.pos:
            return float(self.pos[:-1])
    
    @deprecated('use get_tdelay()')
    def get_voltage_offset(self):
        return self.get_voffset()
    
    def get_vscale(self):
        if 'uV' in self.scale:
            return float(self.scale[:-2])*1e-6
        if 'mV' in self.scale:
            return float(self.scale[:-2])*1e-3
        if 'V' in self.scale:
            return float(self.scale[:-1])

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
        for k,v in e_dict.items():
            if v.lower() == "on":
                e_dict[k] = True
            if v.lower() == "off":
                e_dict[k] = False
        
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
    
    def get_tdelay(self):
        if 'us' in self.delay:
            return float(self.delay[:-2])*1e-6
        if 'ms' in self.delay:
            return float(self.delay[:-2])*1e-3
        elif 's' in self.delay:
            return float(self.delay[:-1])

    @deprecated('use get_tdelay()')
    def get_time_delay(self):
        return self.get_tdelay()

    def get_tscale(self):
        if 'us' in self.scale:
            return float(self.scale[:-2])*1e-6
        if 'ms' in self.scale:
            return float(self.scale[:-2])*1e-3
        if 's' in self.scale:
            return float(self.scale[:-1])
        
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
        for k,v in e_dict.items():
            if v.lower() == "on":
                e_dict[k] = True
            if v.lower() == "off":
                e_dict[k] = False
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
    


# def _test():
if __name__ == '__main__' :
    
    path = r'data_day_two/scope_110.txt'
    lines = _read_file(path)
    idx = _get_indices(lines)
    
    k = 'HORIZONTAL'
    for k in _KEYWORDS:
        info = _info_from_keyword(k, idx, lines)
        print(_parse_info(k, info), '\n')
        
    p = load_param(path)
    print(f'offset: {p.horizontal.get_tdelay()} s')
    print(f'v-offset: {p.analog[0].get_voffset()} V')

# if __name__ == '__main__' :
    # _test()        