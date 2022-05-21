import random
import numpy as np
import math

from assets import *
from civil_war import Civil_War

class World:
    def __init__(self, size: int):
        """Represents the World where the simulation is run.

        Args:
            size (int): Size of the world.
        """
        self.world = np.ndarray((size, size), dtype=Land)
        self.size = size
        self.wars = []
        self.civil_wars = []
        self.govenment_changes = []
        self.date = 0
        self.continents = []

    def advance(self):
        self.date += 1
        for continent in self.continents:
            continent.advance()

class Continent:
    def __init__(self, name: str, territory: float, population: float, growth: float, income: float, literacy: float, military_spend_gdp: float, government_rate: float, world: World):
        self.name = name
        self.growth = growth
        self.income = income
        self.literacy = literacy
        self.military_spend = military_spend_gdp
        self.government_rate = government_rate
        self.world = world

        self.borders = []
        self.land = []
        self.neighbors = []
        
        self.current_civil_war = None
        self.current_wars = []

        self.peace_time = 0
        self.government_time = 0

        self.sort_lands(territory, population)

    def advance(self):
        self.war_trigger()
        self.civil_war()
        self.government_change()
        self.peace_growth()
    
    def sort_lands(self, territory, population): # Finished
        total_lands = math.ceil(territory / LAND_SIZE)
        land_pop = math.ceil(population / total_lands)
        land_left = territory
        pop_left = population

        size = math.floor(math.sqrt(total_lands))
        
        x = 0
        while land_left > 0:
            for y in range(size):
                if land_left >= LAND_SIZE: temp_land = LAND_SIZE
                else: temp_land = land_left

                if pop_left >= land_pop: temp_pop = land_pop
                else: temp_pop = pop_left

                if temp_land > 0 and temp_pop > 0:
                    self.land.append(Land(temp_land, temp_pop, x, y, self))
                    land_left -= temp_land
                    pop_left -= temp_pop
            x += 1
    
    def territory(self): # Finished
        return sum(land.territory for land in self.land)

    def population(self): # Finished
        return sum(land.population for land in self.land)

    def total_income(self): # Finished
        return self.population() * self.income

    def government_change(self, forced=False, insurgency_win = True): # Finished
        if forced:
            if insurgency_win:
                self.world.govenment_changes.append(Government_Change(self, "Insurgency", INSURGENCY_SUPPORT))
            else:
                self.world.govenment_changes.append(Government_Change(self, "Casualty Threshold"))
            self.government_time = 0
        else:
            self.government_time += 1
            if self.government_time >= (GOVERNMENT_TIME * 365):
                self.government_time = 0
                self.world.govenment_changes.append(Government_Change(self, "Government Election"))

    def border_with(self, neighbor):
        neighboring_land = []
        for border in self.borders:
            neighboring_land.append(land for land in border.neighbors() if land.ruler == neighbor)
        return neighboring_land

    def war_trigger(self):
        income_std = std([c.total_income() for c in self.world.continents])
        for neighbor in self.neighbors:
            if (self.total_income() - neighbor.total_income()) > income_std:
                print("War neighbor")
            elif (self.total_income() - neighbor.total_income()) > (INCOME_THRESHOLD * income_std): self.civil_war(True)
        
        population_std = std([c.population() for c in self.world.continents])
        if self.population() > (population_std + (sum(c.population() for c in self.world.continents) / len(self.world.continents))):
            lowest_income = self
            for neighbor in self.neighbors:
                if neighbor.total_income() < lowest_income.total_income(): lowest_income = neighbor

            if not lowest_income == self: print("War lowest_income")
            else: self.civil_war(True)

    def civil_war(self, new=False): # Finished
        if new:
            self.current_civil_war = Civil_War(self)
            self.world.civil_wars.append(self.current_civil_war)
        elif self.current_civil_war:
            self.current_civil_war.continue_war()
            if self.current_civil_war.state == 2: self.current_civil_war = None

    def peace_growth(self): # Finished
        self.peace_time += 1
        if self.peace_time >= (PEACE_TIME * 365):
            self.peace_time = 0
            self.literacy += std([c.literacy for c in self.world.continents]) / 10
            self.income += std([c.income for c in self.world.continents]) / 8

            if self.literacy < 0.4: self.growth += self.growth / 3
            if self.literacy > 0.4 and self.literacy < 0.7: self.growth += self.growth / 6
            if self.literacy > 0.7 and self.literacy < 0.9: self.growth -= self.growth / 6
            if self.literacy > 0.9: self.growth -= self.growth / 3

class Land:
    def __init__(self, territory: float, population: float, x: int, y: int, ruler: Continent):
        self.territory = territory
        self.population = population
        self.x = x
        self.y = y
        self.ruler = ruler

        self.ruler.world.world[self.x, self.y] = self

    def change_ruler(self, other: Continent):
        self.ruler = other

    def grow(self):
        self.population += self.population * (self.ruler.growth / 100) / 12
    
    def total_income(self):
        return self.population * self.ruler.income
    
    def military_spending(self):
        return (self.ruler.military_spend / 100) * self.total_income()

    def neighbors(self):
        neighboring_land = []
        if self.x > 0:
            if type(self.ruler.world.world[self.x - 1, self.y]) == Land: neighboring_land.append(self.ruler.world.world[self.x - 1, self.y])
        if self.x < self.ruler.world.size:
            if type(self.ruler.world.world[self.x + 1, self.y]) == Land: neighboring_land.append(self.ruler.world.world[self.x + 1, self.y])
        if self.y > 0:
            if type(self.ruler.world.world[self.x, self.y - 1]) == Land: neighboring_land.append(self.ruler.world.world[self.x, self.y - 1])
        if self.y < self.ruler.world.size:
            if type(self.ruler.world.world[self.x, self.y + 1]) == Land: neighboring_land.append(self.ruler.world.world[self.x, self.y + 1])
        return neighboring_land

    def cwi(self, insurgency_boost=1):
        if random.random() < (LUCK / 100): luck = BOOST * insurgency_boost
        else: luck = 1
        return self.total_income() * self.ruler.government_rate * (self.ruler.literacy / 100) * self.military_spending() * luck

    def __repr__(self):
        return f"Land of {self.ruler.name} in ({self.x}, {self.y})"

class Government_Change:
    def __init__(self, continent: Continent, reason: str, insurgency_boost=0):
        """Represents a Government Change of a Continent.

        Args:
            continent (Continent): The Continent that will change government.
            reason (str): The reason the Government Change happens.
            insurgency_boost (int, optional): The boost given when a Civil War is won by the insurgents. Defaults to 0.
        """
        self.continent = continent
        self.reason = reason
        self.insurgency = insurgency_boost
        self.past_government = self.continent.government_rate
        self.new_government = random.random() + insurgency_boost

        self.continent.government_rate = self.new_government

    def __repr__(self):
        """Representation in a string the information of a Government Change.

        Returns:
            str: The string representation of a Government Change.
        """
        return f"Government change from {self.continent.name} due to {self.reason}\nPast: {self.past_government}\nNew: {self.new_government}\n"