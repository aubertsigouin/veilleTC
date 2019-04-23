#%% GET TRAINING SET

from langdetect import detect
import pandas as pd
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import re 

def get_training_data():
    
    veilles = os.listdir('../data/training_set')
    
    df_list = []
    other = []
    
    for v in range(len(veilles)):
        print(veilles[v])
        for sheet in range(2):
            df = pd.read_excel('../data/training_set/{}'.format(veilles[v]),sheet)
            df_list.append(df[df['category']=='Ressources humaines et milieu de travail'])
            other.append(df[df['category']!='Ressources humaines et milieu de travail'])

    df = pd.concat(df_list).reset_index(drop=True)
    test = pd.concat(other).sample(1000).reset_index(drop=True)
    other = pd.concat(other).sample(60).reset_index(drop=True)
    
    
    def get_lemmatized_words(df):
        l = []
        for x in range(len(df)):
            txt = df['description'][x].lower()
            txt = re.sub(r'\d+', '', txt)
            
            import string
            txt = txt.translate(str.maketrans('', '', string.punctuation))
            txt = txt.strip()
            txt
            
            from nltk.tokenize import word_tokenize
            from nltk.corpus import stopwords
            
            stopWords = set(stopwords.words('english'))
            stopWords_fr = set(stopwords.words('french'))
            words = word_tokenize(txt)
            wordsFiltered = []
             
            for w in words:
                if w not in stopWords:
                    if w not in stopWords_fr:
                        wordsFiltered.append(w)
             
            txt = ' '.join(wordsFiltered)
            txt
            
            from nltk.stem import WordNetLemmatizer
            from nltk.tokenize import word_tokenize
            
            lemmatizer=WordNetLemmatizer()
            
            txt=word_tokenize(txt)
            for word in txt:
                l.append(lemmatizer.lemmatize(word))
            
        return(list(set(l)))
    
    all_lems = get_lemmatized_words(df=df)
    #pd.DataFrame(all_lems).to_excel('lems.xlsx')

    def preprocess(df, lems):
        
        for x in range(len(df)):
    
            txt = df['description'][x].lower()
            txt = re.sub(r'\d+', '', txt)
            
            import string
            txt = txt.translate(str.maketrans('', '', string.punctuation))
            txt = txt.strip()
            txt
    
            stopWords = set(stopwords.words('english'))
            stopWords_fr = set(stopwords.words('french'))
            words = word_tokenize(txt)
            wordsFiltered = []
             
            for w in words:
                if w not in stopWords:
                    if w not in stopWords_fr:
                        wordsFiltered.append(w)
             
            txt = ' '.join(wordsFiltered)
            txt
    
            lemmatizer=WordNetLemmatizer()
            l=[]
            txt=word_tokenize(txt)
            for word in txt:
                l.append(lemmatizer.lemmatize(word))
                
            def is_in(word,txt):
                if word in txt:
                    return 1
                else :
                    return 0
                
            for z in range(len(lems)):
                df.loc[x,lems[z]] = is_in(lems[z], l)
        return(df)
        
    df['is_hr'] = 1
    
    df = preprocess(df=df, lems=pd.read_excel('../lems.xlsx')[0])
    other['is_hr'] = 0
    other = preprocess(df=other, lems=pd.read_excel('../lems.xlsx')[0])
            
    sets = pd.concat([other,df])
    
    return(sets)

#%%

#train_df = get_training_data()
#train_df.to_csv('train_data.csv')
#train_df = pd.read_csv('train_data.csv',index_col=0)
#%%
#from tpot import TPOTClassifier
#from sklearn.model_selection import train_test_split
#
#X_train, X_test, y_train, y_test = train_test_split(train_df.iloc[:,17:], train_df.iloc[:,16],
#                                                    train_size=0.75, test_size=0.25)
#
#tpot = TPOTClassifier(generations=5, population_size=50, verbosity=2)
#tpot.fit(X_train, y_train)
#print(tpot.score(X_test, y_test))
#tpot.export('tpot_hr_pipeline.py')


#%% CODE POUR EXTRACTION D'ENTITÉS

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from tpot.builtins import StackingEstimator, ZeroCount


def preprocess_new_obs(df, all_lems=list(pd.read_excel('../lems.xlsx')[0])):
    for x in range(len(df)):
        
        txt = df['description'][x].lower()
        txt = re.sub(r'\d+', '', txt)
        
        import string
        txt = txt.translate(str.maketrans('', '', string.punctuation))
        txt = txt.strip()
        txt
        
        stopWords = set(stopwords.words('english'))
        stopWords_fr = set(stopwords.words('french'))
        words = word_tokenize(txt)
        wordsFiltered = []
         
        for w in words:
            if w not in stopWords:
                if w not in stopWords_fr:
                    wordsFiltered.append(w)
         
        txt = ' '.join(wordsFiltered)
        txt
        
        lemmatizer=WordNetLemmatizer()
        l=[]
        txt=word_tokenize(txt)
        for word in txt:
            l.append(lemmatizer.lemmatize(word))
            
        def is_in(word,txt):
            if word in txt:
                return 1
            else :
                return 0
            
        for z in range(len(all_lems)):
            df.loc[x,all_lems[z]] = is_in(all_lems[z], l)
    return(df)



def predict_probabilities(new_obs, train_df,all_lems=list(pd.read_excel('../lems.xlsx')[0])):

    exported_pipeline = make_pipeline(
        StandardScaler(),
        StackingEstimator(estimator=LogisticRegression(C=10.0, dual=False, penalty="l2")),
        ZeroCount(),
        MinMaxScaler(),
        StackingEstimator(estimator=LogisticRegression(C=10.0, dual=False, penalty="l2")),
        ExtraTreesClassifier(bootstrap=False, criterion="gini", max_features=0.6500000000000001, min_samples_leaf=1, min_samples_split=13, n_estimators=100)
    )

    exported_pipeline.fit(train_df.iloc[:,-len(all_lems):], train_df.iloc[:,16])
    print(train_df.iloc[:,16])
    results = exported_pipeline.predict_proba(new_obs.iloc[:,-len(all_lems):])
    
    return(results)


#%%
#test_df = pd.read_excel('data/training_set/20190308.xlsx', 1)
#test_df = preprocess_new_obs(test_df)
#score = predict_probabilities(new_obs=test_df,train_df=train_df)
#score = np.array(list(map(lambda x: score[x][0], range(len(score)))))
#preds = test_df[score<0.5].reset_index(drop=True)

#def extract_entities(df, desc_col, col_names, lang, view):
#    meta_list = [[],[],[],[]]
#    if lang == 'fr':
#        nlp_fr = fr_core_news_md.load()
#        for row in range(len(df)):
#            doc = nlp_fr(df['description'][row])
#            labels = [x.label_ for x in doc.ents]
#            items = [x.text for x in doc.ents]
#            meta_list[0].append([(X.text, X.label_) for X in doc.ents])
#            meta_list[1].append((Counter(labels)))
#            meta_list[2].append(Counter(items).most_common(5))
#            if view == 'True':
#                displacy.render(doc, jupyter=True, style='ent')
#            else :
#                pass
#            array = []
#            for token in doc:
#                array.append(np.array(
#                [token.text, token.lemma_, 
#                token.pos_, token.tag_, 
#                token.dep_, token.shape_, 
#                token.is_alpha, token.is_stop]))
#            meta_list[3].append(array)
#    if lang == 'en':
#        nlp_en = en_core_web_md.load()
#        for row in range(len(df)):
#            doc = nlp_en(df['description'][row])
#            labels = [x.label_ for x in doc.ents]
#            items = [x.text for x in doc.ents]
#            meta_list[0].append([(X.text, X.label_) for X in doc.ents])
#            meta_list[1].append((Counter(labels)))
#            meta_list[2].append(Counter(items).most_common(5))
#            if view == 'True':
#                displacy.render(doc, jupyter=True, style='ent')
#            else :
#                pass
#            array = []
#            for token in doc:
#                array.append(np.array(
#                [token.text, token.lemma_, 
#                token.pos_, token.tag_, 
#                token.dep_, token.shape_, 
#                token.is_alpha, token.is_stop]))
#            meta_list[3].append(array)
#    df[col_names[0]] = meta_list[0]
#    df[col_names[1]] = meta_list[1]
#    df[col_names[2]] = meta_list[2]
#    df[col_names[3]] = meta_list[3]
#    
#    
#    return(df)