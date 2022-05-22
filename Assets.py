import math
import numpy as np
import random
from configuration import *

def get_date(days):
    years = int(days/365)
    days = days - (365*years)
    for i, x in enumerate(MONTHS):
        if days <= x:
            days = days - MONTHS[i-1]
            return(str(days) + "/" + str(i) + "/" + str(years))
    return "0"

def std(array):
    mean = sum(array) / len(array)
    return math.sqrt( (sum(abs(a - mean)**2 for a in array)) / len(array) )

def addArray(worldArr, x, y):
    n, _ = np.shape(worldArr)
    pivotX = random.randint(0, n-x)
    pivotY = random.randint(0, n-y)
    newArray = worldArr[pivotX:pivotX+x, pivotY:pivotY+y]
    if np.sum(newArray) == 0:
        worldArr[pivotX:pivotX+x, pivotY:pivotY+y] = 1
    return worldArr
