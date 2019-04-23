from langdetect import detect

def detectlang(df, col_name, desc_col):
    for x in range(len(df)):
        try :
            df.loc[x,col_name] = detect(df[desc_col][x])
        except:
            df.loc[x,col_name] = 'None'
            print('error while detecting languages')
   
    return(df)
    
#%% CODE POUR EXTRACTION D'ENTITÉS
    
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