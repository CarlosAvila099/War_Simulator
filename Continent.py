import random
from Configuration import *

class Continent:
    def __init__(self, name: str, territory: int, population: int, growth: float, income: float, literacy: float, military_spend_gdp: float, government_rate: float):
        """Represents a continent in the simulation.

        Args:
            name (string): The continents name.
            territory (int): The size of the territory in km^2
            population (int): The size of popultation.
            growth (float): The growth rate of the pupolation, percentage.
            income (float): The income per capita.
            literacy (float): The literacy rate of the population, percentage.
            military_spend_gdp (float): The military spend % of GDP.
            government_rate (float): A value from 0 to 1 to determine the strength of the govenrment.
        """
        self.name = name
        self.territory = territory
        self.population = population
        self.__growth = growth
        self.__income = income
        self.__literacy = literacy
        self.__military_spend = military_spend_gdp
        self.__government_rate = government_rate

        self.borders = []
        self.__growth_counter = 0
        self.__peace_time = 0
        self.__government_change = 0

    def total_income(self):
        return self.population * self.__income

    def gdp(self):
        return 
    
    def military_spending(self):
        return self.__military_spend * self.gdp()

    def cwi(self):
        if random.random() < (LUCK / 100): luck = BOOST
        else: luck = 1
        
        return self.total_income() * self.__government_rate * self.__literacy * self.military_spending() * luck

    def __govenment_change(self):
        if self.__government_change == 5: 
            self.__government_rate = random.random()
            self.__government_change = 0

    def __peace_growth(self):
        if self.__peace_time == 10:
            self.__peace_time = 0

    def __grow(self):
        if self.__growth_counter == 1:
            self.population += self.population * self.__growth / 12
            self.__growth_counter = 0