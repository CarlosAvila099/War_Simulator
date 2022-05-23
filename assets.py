import math
from configuration import *

def get_date(days):
    years = int(days/365)
    days = days - (365*years)
    for i, x in enumerate(MONTHS):
        if days <= x:
            days = days - MONTHS[i-1]
            return(str(days) + "/" + str(i) + "/" + str(years))
    return "0"

def std(array: list):
    """Calculates the standard deviation of a list.

    Args:
        array (list): The list containing the values needed for the standard deviation.

    Returns:
        float: The standard deviation of the list.
    """
    mean = sum(array) / len(array)
    return math.sqrt( (sum(abs(a - mean)**2 for a in array)) / len(array) )