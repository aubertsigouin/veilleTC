# -*- coding: utf-8 -*-
"""
Crée le 13 mars 2019

@auteur: Aubert Sigouin-Lebel

Extrait les récents articles d'une liste de flux RSS et applique un système
de scoring mesurant l'intérêt pour TC

Paramètres :
    xlsx_out (*str*) : chemin du fichier Excel crée
    
    rss_path (*str*) : chemin menant au fichier Excel des flux RSS
    
    keyword_path (*str*) : chemin menant au fichier Excel des keywords (prédicteurs)
    
    stopword_path (*str*) : chemin menant au fichier Excel des stopwords
    
    heure (*int*) : seuil horaire

Sortie :
    Un fichier Excel à l'adresse data/YY/MM/DD/, comportant différentes feuilles
    et en triant les articles selon la pertinence en vertu de l'occurence des termes choisis.


"""

#%% IMPORTATION DES MODULES

    # Code d'Aubert

from utils.time_tools import date, is_monday
from utils.clean import clean
from utils.path_handling import create_path
from extract.extract import extract_articles
from metrics.time_filter import time_filter
from metrics.scoring import write_scoring, get_keywords
from metrics.separate import separate
from xls_io.write import write_to_excel

    # Autres modules
    
import sys
from timeit import default_timer as timer
import pandas as pd
import numpy as np
import os

    # Aller dans le dossier parent

sys.path.append("..")   
os.chdir("..")

#%% DÉFINITION D'UN WRAPPER
    
def wrapper(xlsx_out, rss_path, keyword_path, stopword_path, heure):
    
    # Extraire tout les articles
    rss_list = list(pd.read_excel(rss_path)[0])
    df = extract_articles(rss_list)

    # Nettoyer le titre et la description
    df = clean(df = df, col_list = ['title', 'description'])
    df = df.replace('', np.nan, regex=True).dropna(subset=['title', 'description']).reset_index(drop=True)
    
    # Filtrer selon le temps
    df = time_filter(df = df, time_col='pubdate',heure = heure)
    
    # Scorer les articles
    df = write_scoring(
            df = df, 
            col_names = ['score', 'keyword_counts'], 
            title_col = 'title', 
            desc_col = 'description', 
            keyword_list = get_keywords(
                    key_path = keyword_path,
                    stop_path = stopword_path
                    )
            ).reset_index(drop=True)
        
    df.to_excel('test1.xlsx')
        
    # Séparer en différents DataFrame(EN, FR, QC)
    df = separate(df)

    # Écrire en format Excel
    write_to_excel(df_list = df, path = xlsx_out)

#%% PRÉPARATION

    # Dossier pour l'output
create_path()

    # Date pour l'output
today = date()

    # Seuil horaire avec exception si Lundi
if is_monday() == True:
    nb_heure = 24+24+24
else:
    nb_heure = 24

#%% EXÉCUTION MINUTÉE 
    
start = timer()

wrapper(
    xlsx_out = 'data/{}/{}/{}/'.format(*today) + ''.join(today),
    rss_path = 'src/params/rssLinks.xlsx',
    keyword_path = 'src/params/keywords.xlsx', 
    stopword_path = 'src/params/stopwords.xlsx', 
    heure = nb_heure

)

end = timer()


total_time = end - start
mins, secs = divmod(total_time, 60)
hours, mins = divmod(mins, 60)
sys.stdout.write("Total running time: %d:%d:%d.\n" % (hours, mins, secs))