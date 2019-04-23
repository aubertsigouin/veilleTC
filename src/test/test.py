import sys
sys.path.append("..")

from utils.http import get_response
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint

def opmlToList(path):
    l = [] # Initialise une liste
    
    parsedOPML = BeautifulSoup( # Enveloppe avec BS le résultat
        open(path, 'r').read(), # De l'ouverture du fichier OPML
        "lxml-xml"              # Avec un parser XML
    )
    
    for links in parsedOPML.find_all('outline'): # Pour toutes les balises « outline »,
        l.append(links['xmlUrl'])                # Insère la classe xmlUrl dans la liste

    return(l) # Retourne la liste

def verifyRSS(link):
	
    reponse = get_response(link)
    version = reponse.rss['version']
    
    return(link)

def testLinks(url_list):
    
    verified_links = [] # Initialise une liste
    
    for url in range(len(url_list)):      
        try: # Pour les URL de la liste,
            verified_links.append(verifyRSS(url_list[url]))      # 7 Et d'insérer le lien dans la liste
        except :
            pass

    return(verified_links)
   
def getTestedRSS(rss_path_list, out_file):
    liensURL = opmlToList(path = rss_path_list[0]) + opmlToList(path = rss_path_list[1])
    uniques = list(set(liensURL))
    pprint(uniques[:5])
    print('...\n{} éléments trouvés'.format(len(uniques)))
    liensRSS = testLinks(url_list = uniques)
    print('{} éléments restants'.format(len(liensRSS)))
    pd.DataFrame(liensRSS).to_excel(out_file)
    print('enregistré : {}'.format(out_file))