import requests
from bs4 import BeautifulSoup
 
def get_response(url):
    requete = requests.get(url, timeout=5)    
    requete.encoding = 'utf-8'
    
    return(BeautifulSoup(requete.text,"lxml-xml"))
    
    
    
    
