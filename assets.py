import contextlib
import math
from configuration import *
from configuration import STORY_SET, DURATION

class Story_Continent:
    def __init__(self, name):
        self.name = name
        self.population = []
        self.territory = []
        self.military = []
        self.income = []

        self.__pos = 0
        self.__cont = 0

    def add_day(self):
        self.population.append(0)
        self.territory.append(0)
        self.military.append(0)
        self.income.append(0)

    def add_info(self, info: dict):
        self.population[self.__pos] += info['population']
        self.territory[self.__pos] += info['territory']
        self.military[self.__pos] += info['military']
        self.income[self.__pos] += info['income']

    def add_continent(self, continent):
        self.population[self.__pos] += continent.population[self.__pos]
        self.territory[self.__pos] += continent.territory[self.__pos]
        self.military[self.__pos] += continent.military[self.__pos]
        self.income[self.__pos] += continent.income[self.__pos]

        if continent.get_day(self.__pos): self.__cont += 1

    def end_day(self):
        if self.__cont > 0:
            self.population[self.__pos] /= self.__cont
            self.territory[self.__pos] /= self.__cont
            self.military[self.__pos] /= self.__cont
            self.income[self.__pos] /= self.__cont
            self.__cont = 0
        else:
            self.population[self.__pos] /= STORY_SET
            self.territory[self.__pos] /= STORY_SET
            self.military[self.__pos] /= STORY_SET
            self.income[self.__pos] /= STORY_SET
        self.__pos += 1
    
    def get_day(self, day: int):
        return (self.population[day] + self.territory[day] + self.military[day] + self.income[day]) > 0
    
    def get_average(self):
        average = {
            'population': sum(self.population) / DURATION,
            'territory': sum(self.territory) / DURATION,
            'military': sum(self.military) / DURATION,
            'income': sum(self.income) / DURATION
        }
        return average

    def __repr__(self):
        return f"{self.name}, P: {self.population}, T: {self.territory}, M: {self.military}, I: {self.income}"

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