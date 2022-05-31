import math
from assets import std
from configuration import STALE_TIME

class Battle:
    def __init__(self, land1, land2, date: int):
        """Represents a Battle of a War.

        Args:
            land1 (Land): A Land that will fight in the Battle.
            land2 (Land): A Land that will fight in the Battle.
            date (int): The relative date of the War when the Battle started.
        """
        self.starting_date = date
        self.land1 = land1
        self.land2 = land2
        self.continent1 = land1.ruler
        self.continent2 = land2.ruler

        self.land1_cwi = 0
        self.land2_cwi = 0

        self.winner = None
        self.loser = None
        self.land_won = None
        self.casualties_win = 0
        self.casualties_lose = 0

        self.__outcome()

    def __calculate_casualties(self, winner_cwi: float, loser_cwi: float, winner_pop: int, loser_pop: int):
        """Calculates the casualties depending on the winner and the loser.

        Args:
            winner_cwi (float): The CWI of the winner side.
            loser_cwi (float): The CWI of the loser side.
            winner_pop (int): The population of the winner side.
            loser_pop (int): The population of the loser side.
        """
        df = loser_cwi / winner_cwi
        self.casualties_win = math.floor((1 - df) * df * winner_pop)
        self.casualties_lose = math.floor(df * loser_pop)

    def __outcome(self):
        """Defines the outcome of the Battle.
        """
        self.land1_cwi = self.land1.cwi()
        self.land2_cwi = self.land2.cwi()
        if self.land1_cwi > self.land2_cwi:
            self.winner = self.continent1
            self.loser = self.continent2
            self.land_won = self.land2
            self.__calculate_casualties(self.land1_cwi, self.land2_cwi, self.land1.population, self.land2.population)
            self.land1.population -= self.casualties_win
            self.land2.population -= self.casualties_lose
            
        elif self.land1_cwi == self.land2_cwi:
            self.land1.population -= self.land1.population / 2
            self.land2.population -= self.land2.population / 2
        else:
            self.winner = self.continent2
            self.loser = self.continent1
            self.land_won = self.land1
            self.__calculate_casualties(self.land2_cwi, self.land1_cwi, self.land1.population, self.land2.population)
            self.land1.population -= self.casualties_lose
            self.land2.population -= self.casualties_win

    def __repr__(self):
        """Represents in a string the information of the Battle.

        Returns:
            str: The string representing the Battle.
        """
        return f"Battle between {self.continent1} and {self.continent2}, day {self.starting_date} of War\n{self.continent1} in {self.land1}: {self.land1_cwi}\n{self.continent2} in {self.land2}: {self.land2_cwi}\nWinner: {self.winner} with {self.casualties_win} casualties\nLoser: {self.loser} with {self.casualties_lose} casualties\n"
    
    def to_json(self):
        """Creates a string in JSON format of the Battle.

        Returns:
            str: The JSON format.
        """
        if self.winner: 
            winner = self.winner.name
            loser = self.loser.name
        else:
            winner = ""
            loser = ""
        
        if self.land_won: land_won = self.land_won.to_json()
        else: land_won = ""

        json = f'''
        "starting_date": {self.starting_date},
        "land1": ''' + "{" + self.land1.to_json() + "}" + f''',
        "land2": ''' + "{" + self.land2.to_json() + "}" + f''',
        "continent1": "{self.continent1.name}",
        "continent2": "{self.continent2.name}",
        "land1_cwi": {self.land1_cwi},
        "land2_cwi": {self.land2_cwi},
        "winner": "{winner}",
        "loser": "{loser}",
        "land_won": ''' + "{" + land_won + "}" + f''',
        "casualties_win": {self.casualties_win},
        "casualties_lose": {self.casualties_lose}
        '''
        return json

class War:
    def __init__(self, continent1, continent2, reason: str):
        """Represents a War of the simulation.

        Args:
            continent1 (Continent): A Continent that will fight the War.
            continent2 (Continent): A Continent that will fight the War.
            reason (str): The reason the War started.
        """
        self.continent1 = continent1
        self.continent2 = continent2
        self.starting_date = continent1.world.date
        self.reason = reason

        self.__continent1_land_start = len(continent1.land) # Starting territory of Continent 1, used in end conditions.
        self.__continent2_land_start = len(continent2.land) # Starting territory of Continent 2, used in end conditions.

        self.continent1_wins = 0
        self.continent2_wins = 0
        self.ties = 0
        self.days = 0
        self.battles = []
        self.war_win = None
        
        self.end = False
        self.end_reason = ""

        self.continue_war()

    def casualties(self, continent):
        """Calculates the casualties of the Continent given.

        Args:
            continent (Continent): The Continent whose casualties will be calculated.

        Returns:
            int: The sum of all the casualties suffered throughout the War.
        """
        casualties = 0
        for battle in self.battles:
            if battle.winner == continent: casualties += battle.casualties_win
            elif battle.loser == continent: casualties += battle.casualties_lose
        return casualties

    def continue_war(self):
        """Advances the War by a day and checks if the end conditions are met.
        """
        if not self.end:
            self.days += 1
            self.__battle()
            self.__check_end()

    def __add_battle(self, battle: Battle):
        """Updates the statistics of the War.

        Args:
            battle (Battle): The Battle that will be taken into account to update statistics.
        """
        self.battles.append(battle)
        if battle.winner == self.continent1:
            self.continent1_wins += 1
            self.continent2.leave_land(battle.land_won)
            self.continent1.add_land(battle.land_won)
        elif battle.winner == self.continent2:
            self.continent2_wins += 1
            self.continent1.leave_land(battle.land_won)
            self.continent2.add_land(battle.land_won)
        else: self.ties += 1

    def __battle(self):
        """Creates a Battle for every border that the Continents have with one another.
        """
        for battle in self.continent1.border_with(self.continent2):
            self.__add_battle(Battle(battle[0], battle[1], self.days))

    def __check_end(self):
        """Determines if the War has ended.
        """
        if len(self.continent1.land) <= (self.__continent1_land_start / 2):
            self.end = True
            self.war_win = self.continent2
            self.continent2.annex_continent(self.continent1)
            self.end_reason = "Annexation"
        elif len(self.continent2.land) <= (self.__continent2_land_start / 2):
            self.end = True
            self.war_win = self.continent1
            self.continent1.annex_continent(self.continent2)
            self.end_reason = "Annexation"
        elif self.continent1.total_income() > (self.continent2.total_income() + 3 * std([c.total_income() for c in self.continent1.world.continents])):
            self.end = True
            self.war_win = self.continent1
            self.continent2.government_change(self.starting_date + self.days, True, 3)
            self.end_reason = "Income Stop"
        elif self.continent2.total_income() > (self.continent1.total_income() + 3 * std([c.total_income() for c in self.continent1.world.continents])):
            self.end = True
            self.war_win = self.continent2
            self.continent1.government_change(self.starting_date + self.days, True, 3)
            self.end_reason = "Income Stop"
        elif len(self.battles) >= STALE_TIME:
            counter = 0
            for battle in self.battles[-STALE_TIME:]:
                if battle.winner == None: counter += 1
                
            if counter == STALE_TIME:
                self.end = True
                self.end_reason = "Stale State Stop"
                self.continent1.government_change(self.starting_date + self.days, True, 4)
                self.continent2.government_change(self.starting_date + self.days, True, 4)

    def __repr__(self):
        """Represents in a string all the information of the War.

        Returns:
            str: The string representation of a War.
        """
        return f"War between {self.continent1} and {self.continent2} on date {self.starting_date} due to {self.reason}. Ended on day {self.days} of the War, with {self.war_win} as a winner due to {self.end_reason}."

    def to_json(self):
        """Creates a string in JSON format of the War.

        Returns:
            str: The JSON format.
        """
        json = f'''
        "continent1": "{self.continent1.name}",
        "continent2": "{self.continent2.name}",
        "start_date": {self.starting_date},
        "reason": "{self.reason}",
        "war_win": "{self.war_win}",
        "days": {self.days},
        "end_reason": "{self.end_reason}",
        "continent1_win": {self.continent1_wins},
        "continent2_win": {self.continent2_wins},
        "ties": {self.ties},
        "end": "{self.end}",
        "casualties1": {self.casualties(self.continent1)},
        "casualties2": {self.casualties(self.continent2)},
        "battles": [
        '''
        for battle in self.battles:
            json += "{" + battle.to_json() + "},"
        if self.battles: json = json[:-1]
        json += '''
        ]'''
        return json