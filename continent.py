import random
import numpy as np
import math

from assets import *
from civil_war import Civil_War
from war import War

class World:
    def __init__(self, size: int, continents: list):
        """Represents the World where the simulation is run.

        Args:
            size (int): Size of the world.
            continents (list): List containing all Continents the World will have.
        """
        self.world = np.ndarray((size, size), dtype=Land)
        self.size = size
        self.wars = []
        self.civil_wars = []
        self.govenment_changes = []
        self.date = 1
        self.continents = continents
        self.__start_world()

    def __start_world(self):
        """Creates the World and the initializes Continents.

        Args:
            random (bool): A flag to determine if Continent creation is random.
        """

        for continent in self.continents:
            continent.world = self
            continent.sort_lands()
            for land in continent.land:
                self.world[land.x, land.y] = land
        
        for continent in self.continents:
            continent.calculate_borders()
            continent.calculate_neighbors()

    def advance(self):
        """Advances the World by a day.
        """
        self.date += 1

        grow = False
        if self.date % 366 in MONTHS: grow = True
        for continent in self.continents:
            if grow:
                for land in continent.land: land.grow()
            continent.advance()

    def get_array(self):
        """Returns the world as an int array to paint in matplotlib.

        Returns:
            numpy.ndarray: An array containing the color values of the Continents.
        """
        temp_array = np.zeros((self.size, self.size), dtype=int)
        for continent in self.continents:
            for land in continent.land:
                temp_array[land.x, land.y] = continent.color
        return temp_array

class Continent:
    def __init__(self, name: str, x: int, y: int, color: int, territory: float, population: int, growth: float, income: float, literacy: float, military_spend_gdp: float, government_rate: float):
        """Represents a Continent of the World.

        Args:
            name (str): The name of the Continent.
            x (int): The starting x position of the Continent.
            y (int): The starting y position of the Continent.
            color (int): A value representing the color of the Continent.
            population (int): The starting population of the Continent.
            territory (float): The starting territory of the Continent in km^2.
            population (int): The starting population of the Continent.
            growth (float): The growth rate of the Continent. Percentage.
            income (float): The income per capita of the Continent.
            literacy (float): The literacy rate of the Continent. Percentage.
            military_spend_gdp (float): The percentage of military spending of a Continent depending on its GDP.
            government_rate (float): A value to determine the strength of the government in a Continent.
            x (int, optional): The starting x position of the Continent. Defaults to -1, meaning random.
            y (int, optional): The starting y position of the Continent. Defaults to -1, meaning random.
        """
        self.name = name
        self.growth = growth
        self.income = income
        self.literacy = literacy
        self.military_spend = military_spend_gdp
        self.government_rate = government_rate
        self.world = None
        self.color = None
        self.__x = x 
        self.__y = y
        self.color = color

        self.borders = []
        self.land = []
        self.neighbors = []
        
        self.current_civil_war = None
        self.current_wars = []

        self.__start_territory = territory
        self.__start_population = population

        self.__peace_time = 0
        self.__government_time = 0

        self.__income_war = None
        self.__population_war = None

    ### Information -------------------------------------------------
    def territory(self):
        """Calculates the territory of all the Lands of the Continent.

        Returns:
            float: The sum of all the territory of the Continent.
        """
        return sum(land.territory for land in self.land)

    def population(self): 
        """Calculates the population of all the Lands of the Continent.

        Returns:
            int: The sum of all the population of the Continent.
        """
        return sum(land.population for land in self.land)

    def total_income(self): 
        """Calculates the total income of the Continent.

        Returns:
            float: The total income of the Continent.
        """
        return self.population() * self.income

    def border_with(self, continent):
        """Finds the Land borders of the Continent with another Continent.

        Args:
            continent (Continent): The Continent whose borders will be found.

        Returns:
            list: A list containing all the borders with the Continent given. Each element is [own border, continent border].
        """
        neighboring_land = []
        visited = []
        for border in self.borders:
            neighbors = [land for land in border.neighbors() if land.ruler == continent]
            for land in neighbors:
                if land not in visited:
                    neighboring_land.append([border, land])
                    visited.append(land)
                    break
        return neighboring_land

    ### Initialization ----------------------------------------------
    def sort_lands(self):
        """Sorts the Lands using the starting values of the Continent.
        """
        total_lands = math.ceil(self.__start_territory / LAND_SIZE)
        pop_size = math.ceil(self.__start_population / total_lands)
        land_left = self.__start_territory
        pop_left = self.__start_population

        size = math.floor(math.sqrt(total_lands))
    
        x = 0
        while land_left > 0:
            for y in range(size):
                if land_left >= LAND_SIZE: temp_land = LAND_SIZE
                else: temp_land = land_left

                if pop_left >= pop_size: temp_pop = pop_size
                else: temp_pop = pop_left

                if temp_land > 0 and temp_pop > 0:
                    self.land.append(Land(temp_land, temp_pop, self.__x + x, self.__y + y, self))
                    land_left -= temp_land
                    pop_left -= temp_pop
            x += 1

    def calculate_borders(self):
        """Finds the Land borders of the Continent. Checks Land by Land.
        """
        for land in self.land:
            neighbors = [neighbor for neighbor in land.neighbors() if neighbor.ruler == self]
            if len(neighbors) < 4: self.borders.append(land)

    def calculate_neighbors(self):
        """Finds the Continent's neighbors using the borders.
        """
        for border in self.borders:
            neighbors = [land for land in border.neighbors() if not land.ruler == self]
            for land in neighbors:
                if land.ruler not in self.neighbors: self.neighbors.append(land.ruler)

    ### Advance -----------------------------------------------------
    def advance(self):
        """Advances the Continent by a day. Continuing conflicts and checking time events and war triggers.
        """
        self.__war_trigger()
        self.war()
        self.civil_war()
        self.__peace_growth()
        self.government_change(self.world.date)

    ### Time Related ------------------------------------------------------
    def __peace_growth(self):
        """Checks if the Continent grows due to peace time.
        """
        if not self.current_civil_war and not self.current_wars: self.__peace_time += 1
        if self.__peace_time >= (PEACE_TIME * 365):
            self.__peace_time = 0
            self.literacy += std([c.literacy for c in self.world.continents]) / 10
            self.income += std([c.income for c in self.world.continents]) / 8

            if self.literacy < 0.4: self.growth += self.growth / 3
            if self.literacy > 0.4 and self.literacy < 0.7: self.growth += self.growth / 6
            if self.literacy > 0.7 and self.literacy < 0.9: self.growth -= self.growth / 6
            if self.literacy > 0.9: self.growth -= self.growth / 3

    def government_change(self, date: int, forced=False, reason=0):
        """Creates a Government Change.

        Args:
            date (int): The date the Government Change is made.
            forced (bool, optional): A flag to separate if the Government Change is forced due to conflicts. Defaults to False.
            reason (int, optional): The reason the Government Change is made. Defaults to 0.
                0: Time.
                1: Civil War won by insurgency.
                2: Civil War ended due to casualty threshold.
                3: War ended by opposing side.
                4: War ended by stale state.
        """
        if forced:
            if reason == 1:
                self.world.govenment_changes.append(Government_Change(date, self,"Insurgency", INSURGENCY_SUPPORT))
            elif reason == 2:
                self.world.govenment_changes.append(Government_Change(date, self, "Civil Casualty Threshold"))
            elif reason == 3:
                self.world.govenment_changes.append(Government_Change(date, self, "Conflict"))
            elif reason == 4:
                self.world.govenment_changes.append(Government_Change(date, self, "Stale State"))
            self.__government_time = 0
        else:
            self.__government_time += 1
            if self.__government_time >= (GOVERNMENT_TIME * 365):
                self.__government_time = 0
                self.world.govenment_changes.append(Government_Change(date, self, "Government Election"))

    def __war_trigger(self):
        """Checks if a War or a Civil War is trigged. It can happend due to income and population triggers.
        """
        income_std = std([c.total_income() for c in self.world.continents])
        for neighbor in self.neighbors:
            if (self.total_income() - neighbor.total_income()) > income_std: self.war(True, neighbor, "Income")
            elif (self.total_income() - neighbor.total_income()) > (INCOME_THRESHOLD * income_std): self.civil_war(True, "Income")
        
        population_std = std([c.population() for c in self.world.continents])
        if self.population() > (population_std + (sum(c.population() for c in self.world.continents) / len(self.world.continents))):
            lowest_income = self
            for neighbor in self.neighbors:
                if neighbor.total_income() < lowest_income.total_income(): lowest_income = neighbor

            if not lowest_income == self: self.war(True, lowest_income, "Population")
            else: self.civil_war(True, "Population")

    ### Civil War -------------------------------------------------------------
    def civil_war(self, new=False, reason=""):
        """Creates a Civil War or advances the current one. Only one Civil War per Continent can be active at a time.

        Args:
            new (bool, optional): A flag to determine whether to create or continue a Civil War. Defaults to False.
            reason (str, optional): The reason the Civil War is created. Defaults to "".
        """
        if new:
            if not self.current_civil_war:
                if (reason == "Income" and not self.__income_war) or (reason == "Population" and not self.__population_war):
                    self.current_civil_war = Civil_War(self, reason)
                    self.world.civil_wars.append(self.current_civil_war)

                    if reason == "Income": self.__income_war = self.current_civil_war
                    elif reason == "Population": self.__population_war = self.current_civil_war
        elif self.current_civil_war:
            self.current_civil_war.continue_war()
            if self.current_civil_war.state == 2:
                if self.__income_war == self.current_civil_war: self.__income_war = None
                elif self.__population_war == self.current_civil_war: self.__population_war = None

                self.current_civil_war = None

    ### War -------------------------------------------------------------------
    def war(self, new=False, continent=None, reason=""):
        """Creates a War or advances current ones. Only one War between two Continents can be active at a time.

        Args:
            new (bool, optional): A flag to determine whether to create or continue a War. Defaults to False.
            continent (Continent, optional): The opposing Continent that will participate in the War. Defaults to None.
            reason (str, optional): The reason the War is created. Defaults to "".
        """
        if new:
            exists = False
            for war in self.current_wars:
                if continent in [war.continent1, war.continent2]: exists = True
            
            if not exists and ((reason == "Income" and not self.__income_war) or (reason == "Population" and not self.__population_war)):
                temp_war = War(self, continent, reason)
                continent.current_wars.append(temp_war)
                self.current_wars.append(temp_war)
                self.world.wars.append(temp_war)

                if reason == "Income": self.__income_war = temp_war
                elif reason == "Population": self.__population_war = temp_war
        else:
            for war in self.current_wars:
                war.continue_war()
                if war.end:
                    if self.__income_war == war: self.__income_war = None
                    elif self.__population_war == war: self.__population_war = None
                    if war in self.current_wars: self.current_wars.remove(war)

    def add_land(self, land):
        """Occupation of a Land, updates Continent Lands and borders.

        Args:
            land (Land): The Land to be occupied.
        """
        land.ruler = self
        self.land.append(land)
        self.borders.append(land)
        self.__repart_population()
        self.__recalculate_borders()

    def __repart_population(self):
        """Redistributes the population in all the Continent.
        """
        pop_size = math.ceil(self.population() / len(self.land))
        pop_left = self.population()

        for land in self.land:
            if pop_left >= pop_size: temp_pop = pop_size
            else: temp_pop = pop_left

            pop_left -= temp_pop
            land.population = temp_pop

    def __recalculate_borders(self):
        """Eliminates the false borders from the border list.
        """
        for land in self.borders:
            neighbors = [neighbor for neighbor in land.neighbors() if neighbor.ruler == self]
            if len(neighbors) == 4: self.borders.remove(land)

    def leave_land(self, land):
        """Leaves a Land, updates Continent Lands and borders. Population seeks refuge in other Lands of the same Continent.

        Args:
            land (Land): The Land that is lost.
        """
        neighbors = [neighbor for neighbor in land.neighbors() if neighbor.ruler == self]
        if len(neighbors) == 0:
            if not self.land[0] == land: temp_land = self.land[0]
            else: temp_land = self.land[1]
            temp_land.population += land.population
        else:
            pop_left = land.population
            pop_size = math.ceil(land.population / len(neighbors))
            for neighbor in neighbors:
                if pop_left >= pop_size: temp_pop = pop_size
                else: temp_pop = pop_left
                
                pop_left -= temp_pop
                land.population -= temp_pop
                neighbor.population += temp_pop
        self.__lose_border(land)

        if len(neighbors) == 0: self.__repart_population()

    def __lose_border(self, land):
        """Removes a Land from the border list of the Continent. Updates borders.

        Args:
            land (Land): The border that will be lost.
        """
        neighbors = [neighbor for neighbor in land.neighbors() if neighbor.ruler == self]
        for neighbor in neighbors:
            if neighbor not in self.borders: self.borders.append(neighbor)

        if land in self.borders: self.borders.remove(land)
        if land in self.land: self.land.remove(land)

    def annex_continent(self, continent):
        """Annexes the Continent given to the Continent.

        Args:
            continent (Continent): The Continent to be annexed.
        """
        for land in continent.land:
            land.ruler = self
            self.land.append(land)
            self.borders.append(land)
        self.__recalculate_borders()

        if continent.current_civil_war:
            continent.current_civil_war.state = 2
            continent.current_civil_war.end_reason = f"Annexation of {continent} by {self}"
            continent.current_civil_war = None
        for war in continent.current_wars: 
            war.end = True
            war.end_reason = f"Annexation of {continent} by {self}"
        continent.current_wars = []

        for neighbor in continent.neighbors:
            if neighbor not in self.neighbors: self.neighbors.append(neighbor)
        
        self.world.continents.remove(continent)
        for c in self.world.continents:
            if continent in c.neighbors: c.neighbors.remove(continent)
            if self not in c.neighbors and not c == self: c.neighbors.append(self)

    ### Extra -----------------------------------------------------------------
    def __repr__(self):
        """Represents in a string all the information of a Continent.

        Returns:
            str: The string representation of a Continent.
        """
        return self.name

class Land:
    def __init__(self, territory: float, population: float, x: int, y: int, ruler: Continent):
        """Represents a Land of a Continent.

        Args:
            territory (float): The territory of the Land in km^2.
            population (float): The population of the Land.
            x (int): The x position of the Land.
            y (int): The y position of the Land.
            ruler (Continent): The Continent ruling the Land.
        """
        self.territory = territory
        self.population = population
        self.x = x
        self.y = y
        self.ruler = ruler

        self.ruler.world.world[self.x, self.y] = self

    def total_income(self):
        """Calculates the total income of the Land.

        Returns:
            float: The total income of the Land.
        """
        return self.population * self.ruler.income
    
    def military_spending(self):
        """Calculates the military spending of a Land.

        Returns:
            float: The Land's military spending
        """
        return (self.ruler.military_spend / 100) * self.total_income()

    def cwi(self, insurgency_boost=1):
        """The Capability of War Index of a Land. CWI determines the victor in a conflict.

        Args:
            insurgency_boost (int, optional): A boost to represent sociial support to the Insurgency. Defaults to 1.

        Returns:
            float: The CWI of the Land.
        """
        if random.random() <= (LUCK * insurgency_boost / 100): luck = BOOST
        else: luck = 1
        return self.total_income() * self.ruler.government_rate * (self.ruler.literacy / 100) * self.military_spending() * luck

    def grow(self):
        """Population growth in the Land.
        """
        self.population += self.population * (self.ruler.growth / 100) / 12

    def neighbors(self):
        """Finds all the neighbors of the Land.

        Returns:
            list: A list containing all the neighbors of the Land. Only those neighbors who are Land.
        """
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

    def __repr__(self):
        """Representation in a string the information of a Land.

        Returns:
            str: The string representation of a Land.
        """
        return f"Land in ({self.x}, {self.y})"

class Government_Change:
    def __init__(self, date: int, continent: Continent, reason: str, insurgency_boost=0):
        """Represents a Government Change of a Continent.

        Args:
            continent (Continent): The Continent that will change government.
            reason (str): The reason the Government Change happens.
            insurgency_boost (int, optional): The boost given when a Civil War is won by the insurgents. Defaults to 0.
        """
        self.date = date
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
        return f"Government change from {self.continent.name} on day {self.date} due to {self.reason}\nPast: {self.past_government}\nNew: {self.new_government}\n"