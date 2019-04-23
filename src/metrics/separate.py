# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 14:21:02 2019

@author: AubertSigouin-Lebel
"""


qc = ['lapresse', 'lesaffaires', 'radio-canada', '.ca', 'journaldemontreal', 'directioninformatique']

def verify(keyword_list, txt):
    # Par défaut
    exists = False
    
    for item in range(len(keyword_list)):
        if keyword_list[item] in txt:
            exists=True
            
    return(exists)

def separate(df):
    df_en = df[list(map(lambda x: verify(keyword_list=qc, txt = df['link'][x])==False, range(len(df))))].reset_index(drop=True)
    df_qc = df[list(map(lambda x: verify(keyword_list=qc, txt = df['link'][x]), range(len(df))))].reset_index(drop=True)
    return([df_en,df_qc])