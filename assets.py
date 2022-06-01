import math
from configuration import *

def get_date(days: int):
    """Formats a number of days into a date.

    Args:
        days (int): The number of days.

    Returns:
        str: The date in str format.
    """
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

def json_array(array: list):
    """Generates a JSON string from an array as a grid, containing only the values of the cell.

    Args:
        array (list): The array to be formatted.

    Returns:
        str: The str containing the array in JSON format.
    """
    json = ""
    for line in array:
        json += "["
        for pixel in line:
            json += f"{pixel},"
        json = json[:-1] + "],"
    json = json[:-1]
    return json