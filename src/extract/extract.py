import sys
sys.path.append("..")

import pandas as pd
from utils.http import get_response
from utils.time_tools import now

#%%    
    
    
def extract_articles(rssList):

    df_list = [] # Initialise une méta-liste

    for rss in range(len(rssList)):             # Pour tous les flux RSS,
        print('{} | Extraction de {}'.format(now(), rssList[rss]))
        try:
            reponse = get_response(rssList[rss])
        except:
            print("Erreur à l'obtention d'une réponse".format(''))
            pass

        df_cols = ['category','RSS_name','RSS_url','title','enclosure','source','creator','pubDate','description','link']
            
        df = parse_XML(
                news_source = reponse, 
                url = rssList[rss], 
                df_cols=df_cols
                )
        
        df_list.append(df) # Insère le DataFrame dans la méta-liste


    return(pd.concat(df_list, sort=False).reset_index(drop=True)) # Fusionne la liste de DataFrame et réinitialise l'index
    
#%%

def parse_XML(news_source, df_cols, url): 
    """Parse the input XML file and store the result in a pandas DataFrame 
    with the given columns. The first element of df_cols is supposed to be 
    the identifier variable, which is an attribute of each node element in 
    the XML data; other features will be parsed from the text content of 
    each sub-element. """
    
    out_df = pd.DataFrame(columns = df_cols)
    
    for article in news_source.find_all('item'): 
        res = []
        res.append('')
        res.append(news_source.find('title').text)
        res.append(url)
        for el in df_cols[3:]: 
            if article.find(el) is not None:
                res.append(article.find(el).text)
            else: 
                res.append(None)
        out_df = out_df.append(pd.Series(res, index = df_cols), ignore_index = True)
        
    return (out_df[['category',	'description','title','RSS_name','pubDate',
                    'enclosure','link', 'source','creator', 'RSS_url']])
