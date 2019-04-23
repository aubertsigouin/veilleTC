import datetime 

def now():
    return (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def date():
    year = now().split()[0].split('-')[0]
    month = now().split()[0].split('-')[1]
    day = now().split()[0].split('-')[2]
    
    return[year,month,day]
    
def is_monday():
    if datetime.datetime.today().weekday() == 0:
        monday = True
    else:
        monday = False
    return(monday)
    