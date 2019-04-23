import datetime
import pandas as pd
from datetime import timedelta


def time_filter(df, time_col, heure):
    

    for x in range(len(df)):
        try :
            df.loc[x,time_col] = datetime.datetime(df[time_col][x][2], df[time_col][x][1], df[time_col][x][0], df[time_col][x][3])
        except:
            df = df.drop(x,axis=0)
            
    df = df.reset_index(drop=True)

    dateMin = datetime.datetime.now() - timedelta(hours=heure)     # Détermine la date limite
    dateMax = datetime.datetime.now() + timedelta(hours=24)                           # Détermine l'heure présente

    df = df[                                   # Garde seulement
        df[time_col] > pd.to_datetime(dateMin)# les articles post-datant la date limite
    ].reset_index(drop=True)

    return (                                        # Garde et retourne
        df[                                         # seulement
            df[                                     # les articles pré-datant 
                time_col] < pd.to_datetime(dateMax) # l'heure actuelle
        ].reset_index(drop=True)
        )