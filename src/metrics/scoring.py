import pandas as pd

def score(txt, title, l):
    keywds = []

    if type(title) != str:
        txt = 'None'
    if type(txt) != str:
        txt = 'None'
    if len(txt) == 0 :
        txt = 'None'
    if len(title) == 0:
        title = 'None'

    score_txt = 0
    score_title = 0 
    
    for y in range(len(l)):
        
        if len(l[y])>2 and l[y] in txt:
            score_txt += 1
            keywds.append(l[y])
                
        if len(l[y])>2 and l[y] in title:
            score_title += 2
            keywds.append(l[y])

        
    score_1 = score_txt+score_title
            
    return score_1, str(pd.Series(keywds).value_counts().to_json())
        

def get_keywords(key_path,stop_path):
    keywords = list(pd.read_excel(key_path)[0].values)
    stopwords = list(pd.read_excel(stop_path)[0].values)
    for x in range(len(stopwords)):
        keywords.remove(stopwords[x])
    
    return(keywords)

def write_scoring(df, col_names, title_col, desc_col, keyword_list):
    df[col_names[0]] = list(
        map(
            lambda x: score(
                txt=df[desc_col][x],
                title=df[title_col][x], 
                l=keyword_list)[0], 
            range(
                len(
                    df
                )
            )
        )
    )

    df[col_names[1]] = list(
        map(
            lambda x: score(
                txt=df[desc_col][x],
                title=df[title_col][x], 
                l=keyword_list)[1], 
            range(
                len(
                    df
                )
            )
        )
    )

    return(df.sort_values(by=col_names[0], ascending=False).reset_index(drop=True).drop_duplicates(subset=title_col))
