import math
import random
from configuration import CASUALTY_STOP, SOCIAL_SUPPORT

class Inner_Battle:
    def __init__(self, land, date: int):
        """Represents a Inner Battle of a Civil War.

        Args:
            land (Land): The Land where the Inner Battle will be.
            date (int): The relative date of the Civil War where the Inner Battle began.
        """
        self.starting_date = date
        self.land = land

        self.winner = None
        self.loser = None
        self.insurgents = 0 # CWI of the insurgents
        self.government = 0 # CWI of the government
        self.casualties = 0

        self.__outcome()

    def __calculate_casualties(self, winner: float, loser: float):
        """Calculates the casualties depending on the winner and the loser.

        Args:
            winner (float): The CWI of the winner side.
            loser (float): The CWI of the loser side.
        """
        df = loser / winner
        self.casualties = math.floor((1 - df) * df * self.land.population * 2)
        self.land.population -= self.casualties

    def __outcome(self):
        """Defines the outcome of the Inner Battle.
        """
        self.insurgents = self.land.cwi(SOCIAL_SUPPORT)
        self.government = self.land.cwi()
        if self.insurgents > self.government:
            self.winner = "Insurgents"
            self.loser = "Government"
            self.__calculate_casualties(self.insurgents, self.government)
        elif self.insurgents == self.government: return
        else:
            self.winner = "Government"
            self.loser = "Insurgents"
            self.__calculate_casualties(self.government, self.insurgents)

    def __repr__(self):
        """Represents in a string the information of the Inner Battle.

        Returns:
            str: The string representation of the Inner Battle.
        """
        return f"Revolt in {self.land} in the {self.starting_date} day of civil war.\nInsurgents: {self.insurgents}\nGovernment: {self.government}\nWinner: {self.winner}\nLoser: {self.loser}\nCasualties: {self.casualties}\n"

    def to_json(self):
        """Creates a string in JSON format of the Inner Battle.

        Returns:
            str: The JSON format.
        """
        if self.winner:
            winner = self.winner
            loser = self.loser
        else:
            winner = ""
            loser = ""

        json = f'''
        "starting_date:" {self.starting_date},
        "land":''' + "{" + self.land.to_json() + "}" + f''',
        "winner": "{winner}",
        "loser": "{loser}",
        "insurgents": {self.insurgents},
        "government": {self.government},
        "casualties": {self.casualties}
        '''
        return json

class Civil_War:
    def __init__(self, continent, reason: str):
        """Represents a Civil War of a Continent.

        Args:
            continent (Continent): The Continent that has the Civil War.
            reason (str): The reason the Civil War started.
        """
        self.continent = continent
        self.starting_date = continent.world.date
        self.reason = reason
        self.__to_visit = [land for land in self.continent.land]

        self.government_wins = 0
        self.insurgent_wins = 0
        self.ties = 0
        self.days = 0
        self.battles = []
        self.war_win = ""

        self.__insurgent_land = []
        self.state = 0 # 0 - Random Walk, 1 - Inner Battles, 2 - End
        self.end_reason = ""

        self.continue_war()

    def casualties(self):
        """Calculates the current casualties of the Civil War.

        Returns:
            int: The number of casualties of the Civil War.
        """
        return sum(battle.casualties for battle in self.battles)

    def continue_war(self):
        """Advances the Civil War by a day and checks if the end conditions are met.
        """
        if not self.state == 2:
            self.days += 1
            if self.state == 0: self.__random_walk()
            elif self.state == 1: self.__neighbor_raising()

            if self.state == 1: self.__check_end()

    def __add_battle(self, battle: Inner_Battle):
        """Updates the statistics of the Civil War.

        Args:
            battle (Inner_Battle): The Inner Battle that will be taken into account to update statistics.
        """
        self.battles.append(battle)
        if battle.winner == "Insurgents":
            if battle.land not in self.__insurgent_land: self.__insurgent_land.append(battle.land)
            self.insurgent_wins += 1
        elif battle.winner == "Government":
            if battle.land in self.__insurgent_land: self.__insurgent_land.remove(battle.land)
            self.government_wins += 1
        else: self.ties += 1

    def __random_walk(self):
        """Selects a random land to revolt from the Continent having the Civil War.
        """
        if len(self.__to_visit) <= (len(self.continent.land) / 2):
            if self.insurgent_wins > 0: self.state = 1
            else: 
                self.war_win = "Government"
                self.state = 2
        else:
            random_land = random.choice(self.__to_visit)
            self.__to_visit.remove(random_land)
            if random.random() >= 0.5: self.__add_battle(Inner_Battle(random_land, self.days))

    def __neighbor_raising(self):
        """Makes a rising in all the neighboring lands of an insurgent land.
        """
        visited = []
        for land in self.__insurgent_land:
            self.__add_battle(Inner_Battle(land, self.days))
            neihboring_land = land.neighbors()
            for neighbor in neihboring_land:
                if neighbor not in self.__insurgent_land and neighbor not in visited and neighbor.ruler == land.ruler:
                    self.__add_battle(Inner_Battle(neighbor, self.days))
                    visited.append(neighbor)
    
    def __check_end(self):
        """Determines if the Civil War has ended.
        """
        if not self.__insurgent_land: 
            self.state = 2
            self.war_win = "Government"
            self.end_reason = "Civil War Deterred"
        elif len(self.__insurgent_land) > (len(self.continent.land) / 3) and self.continent.government_rate <= 0.4:
            self.state = 2
            self.war_win = "Insurgents"
            self.end_reason = "Insurgent Occupation"
            self.continent.government_change(self.days + self.starting_date, True, 1)
        elif len(self.__insurgent_land) > (2 * len(self.continent.land) / 3) and self.continent.government_rate > 0.4:
            self.state = 2
            self.war_win = "Insurgents"
            self.end_reason = "Insurgent Occupation"
            self.continent.government_change(self.days + self.starting_date, True, 1)
        elif self.casualties() >= (self.continent.population() + self.casualties()) * CASUALTY_STOP / 100:
            self.state = 2
            self.war_win = None
            self.end_reason = "Casualty Stop"
            self.continent.government_change(self.days + self.starting_date, True, 2)
    
    def __repr__(self):
        """Represents in a string all the information of the Civil War.

        Returns:
            str: The string representation of a Civil War.
        """
        return f"Civil War of {self.continent} on date {self.starting_date} due to {self.reason}. Ended on day {self.days} of the Civil War, with {self.war_win} as a winner due to {self.end_reason}."

    def to_json(self):
        """Creates a string in JSON format of the Civil War.

        Returns:
            str: The JSON format.
        """
        json = f'''
        "continent": "{self.continent.name}",
        "start_date": {self.starting_date},
        "reason": "{self.reason}",
        "war_win": "{self.war_win}",
        "days": {self.days},
        "end_reason": "{self.end_reason}"
        "state": {self.state},
        "casualties": {self.casualties()},
        "battles": [
        '''
        for battle in self.battles:
            json += "{" + battle.to_json() + "},"
        if self.battles: json = json[:-1] + '''
        ],
        "insurgent_land": [
        '''
        for il in self.__insurgent_land:
            json += "{" + il.to_json() + "},"
        if self.__insurgent_land: json = json[:-1]
        json += '''
        ]'''
        return json