import sys


# --- CODE D'AUBERT -- #

from utils.time_tools import now
from xls_io.write import render_table

# --- AUTRE MODULE --- #
import os
from datetime import datetime


sys.path.append("..")   
os.chdir("..")   


today = datetime.now()

year = now().split()[0].split('-')[0]
month = now().split()[0].split('-')[1]
day = now().split()[0].split('-')[2]


if os.path.isdir('data/{}'.format(year)):
    pass
else:
    os.mkdir('data/{}'.format(year))
    
if os.path.isdir('data/{}/{}'.format(year, month)):
    pass
else:
    os.mkdir('data/{}/{}'.format(year, month))
    
if os.path.isdir('data/{}/{}/{}'.format(year, month, day)):
    pass
else:
    os.mkdir('data/{}/{}/{}'.format(year, month, day))
    

render_table(xls_in = 'data/{}/{}/{}/'.format(year, month, day) + ''.join(now().split()[0].split('-')), 
             xls_out= 'data/{}/{}/{}/'.format(year, month, day) + 'veille_{}.xlsx'.format(''.join(now().split()[0].split('-')))
            )