import re

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def clean(df, col_list):
    # Utilise un parser HTML pour enlever les possibles tags dans le titre.
    for col in range(len(col_list)):
        df[col_list[col]] = list(map(lambda x: cleanhtml(df[col_list[col]][x]).strip(), range(len(df))))

    return(df) # retourne le DataFrame final
