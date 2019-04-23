# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 11:46:20 2019

@author: AubertSigouin-Lebel
"""

import sys
sys.path.append("..")

from utils.time_tools import now
import os


def create_path():    
    os.path.isdir('data') 
    
    year = now().split()[0].split('-')[0]
    month = now().split()[0].split('-')[1]
    day = now().split()[0].split('-')[2]
    
    
    if os.path.isdir('data/{}'.format(year)):
        pass
    else:
        os.mkdir('data/{}'.format(year))
        
    if os.path.isdir('data/{}/{}'.format(year, month)):
        pass
    else:
        os.mkdir('data/{}/{}'.format(year, month))
        
    if os.path.isdir('data/{}/{}/{}'.format(year, month, day)):
        pass
    else:
        os.mkdir('data/{}/{}/{}'.format(year, month, day))
    
    return[year,month,day]
