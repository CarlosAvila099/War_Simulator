from Configuration import *

def get_date(days):
    years = int(days/365)
    days = days - (365*years)
    for i, x in enumerate(MONTHS):
        if days <= x:
            days = days - MONTHS[i-1]
            return(str(days) + "/" + str(i) + "/" + str(years))
    return "0"

date = get_date(9588)
print(date)