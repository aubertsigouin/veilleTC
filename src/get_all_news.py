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
from metrics.nlp import preprocess_new_obs, predict_probabilities
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

    print('Importation des RSS')
    rss_list = list(pd.read_excel(rss_path)[0])
    
    print('Extraction des articles')
    df = extract_articles(rss_list)
    df.to_excel('test.xlsx')

    print('Nettoyage des titres et description')
    
    df.fillna(value='', inplace=True)
    df = clean(df = df, col_list = ['title', 'description'])
    df = df.replace('', np.nan, regex=True).dropna(subset=['title', 'description']).reset_index(drop=True)
    
    print('Filtrer selon le temps')
    df = time_filter(df = df, time_col='pubDate',heure = heure)

    print('Scorer les articles')
    
    df = preprocess_new_obs(df)
    score = predict_probabilities(new_obs=df,train_df=pd.read_csv('train_data.csv', index_col=0).reset_index(drop=True))
    score = np.array(list(map(lambda x: score[x][0], range(len(score)))))
    df['score']= score
    
    df.sort_values(by='score', ascending=False).reset_index(drop=True).to_excel('test1.xlsx')
    print('Écrire en format Excel')
 #   write_to_excel(df_list = df, path = xlsx_out)

#%% PRÉPARATION

    # Dossier pour l'output
create_path()

    # Date pour l'output
today = date()

    # Seuil horaire avec exception si Lundi
if is_monday() == True:
    nb_heure = 24+24+16
else:
    nb_heure = 16

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