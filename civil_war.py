import random
import math

from configuration import CASUALTY_STOP

class Inner_Battle:
    def __init__(self, land, date: int):
        """Represents a Inner Battle of a Civil War

        Args:
            land (Land): The Land where the Inner Battle will be.
            date (int): The relative date of the civil war where the Inner Battle began.
        """
        self.starting_date = date
        self.land = land

        self.winner = None
        self.loser = None
        self.insurgents = 0 # CWI of the insurgents
        self.government = 0 # CWI of the insurgents
        self.casualties = 0

        self.outcome()

    def calculate_casualties(self, winner: float, loser: float):
        """Calculates the casualties depending on the winner and the loser.

        Args:
            winner (float): The CWI of the winner side.
            loser (float): The CWI of the loser side.
        """
        df = loser / winner
        self.casualties = math.floor((1 - df) * df * self.land.population * 2)
        self.land.population -= self.casualties

    def outcome(self):
        """Defines the outcome of the Inner Battle.
        """
        self.insurgents = self.land.cwi(2)
        self.government = self.land.cwi()
        if self.insurgents > self.government:
            self.winner = "Insurgents"
            self.loser = "Government"
            self.calculate_casualties(self.insurgents, self.government)
        elif self.insurgents == self.government: return
        else:
            self.winner = "Government"
            self.loser = "Insurgents"
            self.calculate_casualties(self.government, self.insurgents)

    def __repr__(self):
        """Represents in a string the information of the Inner Battle.

        Returns:
            str: The string representation of the Inner Battle.
        """
        return f"Revolt in {self.land}, day {self.starting_date} of civil war.\nInsurgents: {self.insurgents}\nGovernment: {self.government}\nWinner: {self.winner}\nLoser: {self.loser}\nCasualties: {self.casualties}\n"

class Civil_War:
    def __init__(self, continent):
        """Represents a Civil War of a Continent.

        Args:
            continent (Continent): The Continent that has the Civil War.
        """
        self.continent = continent
        self.starting_date = continent.world.date
        self.to_visit = [land for land in self.continent.land]

        self.government_wins = 0
        self.insurgent_wins = 0
        self.ties = 0
        self.days = 0
        self.battles = []
        self.war_win = ""

        self.insurgent_land = []
        self.state = 0 # 0 - Random Walk, 1 - Inner Battles, 2 - End

        self.continue_war()

    def casualties(self):
        """Calculates the current casualties of the Civil War.

        Returns:
            int: The number of casualties of the Civil War.
        """
        return sum(battle.casualties for battle in self.battles)

    def continue_war(self):
        """Advances the Civil War by a day, and checks if the end conditions are met.
        """
        if not self.state == 2:
            self.days += 1
            if self.state == 0: self.random_walk()
            elif self.state == 1: self.neighbor_raising()

            if self.state == 1: self.check_end()

    def add_battle(self, battle: Inner_Battle):
        """Updates the statistics of the Civil War.

        Args:
            battle (Inner_Battle): The battle that will be taken into account to update statistics.
        """
        self.battles.append(battle)
        if battle.winner == "Insurgents":
            if battle.land not in self.insurgent_land: self.insurgent_land.append(battle.land)
            self.insurgent_wins += 1
        elif battle.winner == "Government":
            if battle.land in self.insurgent_land: self.insurgent_land.remove(battle.land)
            self.government_wins += 1
        else: self.ties += 1

    def random_walk(self):
        """Creates the random walk of a country.
        """
        if len(self.to_visit) <= (len(self.continent.land) / 2):
            if self.insurgent_wins > 0: self.state = 1
            else: 
                self.war_win = "Government"
                self.state = 2
        else:
            random_land = random.choice(self.to_visit)
            self.to_visit.remove(random_land)
            if random.random() >= 0.5: self.add_battle(Inner_Battle(random_land, self.days))

    def neighbor_raising(self):
        """Makes a rising in all the neighboring lands of a insurgent land.
        """
        visited = []
        for land in self.insurgent_land:
            self.add_battle(Inner_Battle(land, self.days))
            neihboring_land = land.neighbors()
            for neighbor in neihboring_land:
                if neighbor not in self.insurgent_land and neighbor not in visited and neighbor.ruler == land.ruler:
                    self.add_battle(Inner_Battle(neighbor, self.days))
                    visited.append(neighbor)
    
    def check_end(self):
        """Determines if the Civil War has ended.
        """
        if not self.insurgent_land: 
            self.state = 2
            self.war_win = "Government"
        elif len(self.insurgent_land) > (len(self.continent.land) / 3) and self.continent.government_rate <= 0.4:
            self.state = 2
            self.war_win = "Insurgents"
            self.continent.government_change(True, True)
        elif len(self.insurgent_land) > (2 * len(self.continent.land) / 3) and self.continent.government_rate > 0.4:
            self.state = 2
            self.war_win = "Insurgents"
            self.continent.government_change(True, True)
        elif self.casualties() >= (self.continent.population() + self.casualties()) * CASUALTY_STOP / 100:
            self.state = 2
            self.war_win = "Casualty Stop"
            self.continent.government_change(True, False)
    
    def __repr__(self):
        battles = ""
        for battle in self.battles:
            battles += f"{battle}\n"
        return f"Civil War of {self.continent.name} in the day {self.starting_date}:\nWinner: {self.war_win}\nBattles:\n{battles}"