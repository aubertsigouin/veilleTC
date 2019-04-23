import sys
sys.path.append("..")

from utils.http import get_response
from utils.time_tools import now
import pandas as pd
import datetime

def parse(newsSource,url,name):
    newsList = [[] for x in range(9)]
    for article in newsSource.find_all('item'):    # Pour tous les articles
        
        if article.title :                                        # Si une balise <title> existe
            newsList[0].append(article.title.get_text())      # Encode l'information dans la liste 0
        else:                                                     # Sinon
            newsList[0].append('')                            # Encode la valeur ''

        if article.enclosure:                                     # Si une balise <enclosure> existe
            newsList[1].append(article.enclosure)             # Encode l'information dans la liste 1
        else:                                                     # Sinon
            newsList[1].append('')                            # Encode la valeur ''

        if article.source :                                       # Si une balise <source> existe
            newsList[2].append(article.source.get_text())     # Encode l'information dans la liste 2  
        else :                                                    # Sinon
            newsList[2].append('')                            # Encode la valeur ''

        if article.creator :                                      # Si une balise <creator> existe
            newsList[3].append(article.creator.get_text())    # Encode l'information dans la liste 3
        else :                                                    # Sinon
            newsList[3].append('')                            # Encode la valeur ''

        if article.pubDate :   
            date_time = pd.to_datetime(article.pubDate.get_text())                                   # Si une balise <pubDate> existe
            newsList[4].append([date_time.day, date_time.month, date_time.year, date_time.hour])    # Encode l'information dans la liste 4
        else :                                                    # Sinon
            newsList[4].append('')                            # Encode la valeur ''

        if article.description :                                  # Si une balise <description> existe
            newsList[5].append(article.description.get_text())# Encode l'information dans la liste 5
        else :                                                    # Sinon
            newsList[5].append('')                            # Encode la valeur ''

        if article.link :                                         # Si une balise <link> existe
            newsList[6].append(article.link.get_text())       # Encode l'information dans la liste 6
        else :                                                    # Sinon
            newsList[6].append('')     
            
        newsList[7].append(url)
        newsList[8].append(name)
            
    return(newsList)
    
#%%    
    

def parse_espresso_jobs():
    espresso_feed = get_response('https://espresso-jobs.com/listing-feeds/?feedId=1/')
    newsList = [[] for x in range(39)]
    for job in espresso_feed.find_all('job'):    # Pour tous les articles
        
        newsList[0].append(job.find('title').get_text(strip=True))
        newsList[1].append(job.find('job-code').get_text(strip=True))
        newsList[2].append(job.find('job-board-name').get_text(strip=True))
        newsList[3].append(job.find('job-board-url').get_text(strip=True))
        newsList[4].append(job.find('detail-url').get_text(strip=True))
        
        for item in job.find_all('description'):
            newsList[5].append(job.find('summary').get_text(strip=True))
            newsList[6].append(job.find('required-skills').get_text(strip=True))
            newsList[7].append(job.find('required-education').get_text(strip=True))
            newsList[8].append(job.find('required-experience').get_text(strip=True))
            newsList[9].append(job.find('full-time').get_text(strip=True))
            newsList[10].append(job.find('part-time').get_text(strip=True))
            newsList[11].append(job.find('flex-time').get_text(strip=True))
            newsList[12].append(job.find('internship').get_text(strip=True))
            newsList[13].append(job.find('volunteer').get_text(strip=True))
            newsList[14].append(job.find('exempt').get_text(strip=True))
            newsList[15].append(job.find('contract').get_text(strip=True))
            newsList[16].append(job.find('permanent').get_text(strip=True))
            newsList[17].append(job.find('temporary').get_text(strip=True))
            newsList[18].append(job.find('telecommute').get_text(strip=True))
        
        for item in job.find_all('compensation'):
            newsList[19].append(job.find('salary-range').get_text(strip=True))
            newsList[20].append(job.find('salary-amount').get_text(strip=True))
            newsList[21].append(job.find('salary-currency').get_text(strip=True))
            newsList[22].append(job.find('benefits').get_text(strip=True))

        for item in job.find_all('location'):
            newsList[23].append(job.find('address').get_text(strip=True))
            newsList[24].append(job.find('city').get_text(strip=True))
            newsList[25].append(job.find('state').get_text(strip=True))
            newsList[26].append(job.find('zip').get_text(strip=True))
            newsList[27].append(job.find('country').get_text(strip=True))
            newsList[28].append(job.find('area-code').get_text(strip=True))
            
        for item in job.find_all('contact'):
            newsList[29].append(job.find('name').get_text(strip=True))
            newsList[30].append(job.find('email').get_text(strip=True))
            newsList[31].append(job.find('hiring-manager-name').get_text(strip=True))
            newsList[32].append(job.find('hiring-manager-email').get_text(strip=True))
            newsList[33].append(job.find('phone').get_text(strip=True))
            newsList[34].append(job.find('fax').get_text(strip=True))
            
        for item in job.find_all('company'):
            newsList[35].append(job.find('name').get_text(strip=True))
            newsList[36].append(job.find('description').get_text(strip=True))
            newsList[37].append(job.find('industry').get_text(strip=True))
            newsList[38].append(job.find('url').get_text(strip=True))

    newsList[5] = newsList[5][1::2]
    newsList[6] = newsList[6][1::2]
    newsList[7] = newsList[7][1::2]
    newsList[8] = newsList[8][1::2]
    newsList[9] = newsList[9][1::2]
    newsList[10] = newsList[10][1::2]
    newsList[11] = newsList[11][1::2]
    newsList[12] = newsList[12][1::2]
    newsList[13] = newsList[13][1::2]
    newsList[14] = newsList[14][1::2]
    newsList[15] = newsList[15][1::2]
    newsList[16] = newsList[16][1::2]
    newsList[17] = newsList[17][1::2]
    newsList[18] = newsList[18][1::2]
    
    
    return(newsList)
    
#%%    
    
def extract_articles(rssList):

    df_list = [] # Initialise une méta-liste

    for rss in range(len(rssList)):             # Pour tous les flux RSS,
        print('{} | Extraction de {}'.format(now(), rssList[rss]))
        try:
            reponse = get_response(rssList[rss])
        except:
            print('error. passed')
            pass
        
        try:
            content_title = reponse.title.text
        except:
            content_title = ''
            print('error. passed')
            
        dataList = parse(newsSource = reponse, url = rssList[rss], name = content_title)
        
        # Pour tous les articles de mon flux ,
        df = pd.DataFrame() # Initialise un DataFrame
        try:
        # -- Peuple le DataFrame avec les différentes listes -- #
            df['category'] = ''
            df['description'] = dataList[5]
            df['title'] = dataList[0]
            df['name'] = dataList[8]
            df['pubdate'] = dataList[4]
            df['image'] = dataList[1]
            df['link'] = dataList[6]
            df['source'] = dataList[2]
            df['creator'] = dataList[3]
            df['RSS'] = dataList[7]

        except:
            print('error. passed', rssList[rss])

        
        df_list.append(df) # Insère le DataFrame dans la méta-liste


    return(pd.concat(df_list, sort=False).reset_index(drop=True)) # Fusionne la liste de DataFrame et réinitialise l'index
    
#%%
#l = parse_espresso_jobs()
#
#df = pd.DataFrame(l).transpose()
#
#
#
#from lxml import html as HTML
#from lxml.html.clean import clean_html
#from lxml.html.clean import Cleaner
#import re
#
#for x in range(len(df)):
#    for y in range(len(list(df.columns))):
#        if len(df.iloc[x,y]) > 0:
#            doc = HTML.document_fromstring((df.iloc[x,y]))
#            cleaner = Cleaner(style=True)
#            doc = clean_html(doc)
#            text = doc.text_content()
#            df.iloc[x,y] = re.sub(' +',' ',text)
#            
#df.to_excel('data/espresso_jobs/{}.xlsx'.format(''.join(now().split()[0].split('-'))))

