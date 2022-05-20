class Battle:
    def __init__(self, land1, land2):
        self.continent1 = land1.ruler
        self.continent2 = land2.ruler
        self.land1 = land1
        self.land2 = land2

        self.winner = None
        self.loser = None
        self.land_won = None
        self.casualties_win = 0
        self.casualties_lose = 0

    def calculate_casualties(self, winner, loser):
        df = loser.cwi() / winner.cwi()
        self.casualties_win = (1 - df) * df * winner.population
        self.casualties_lose = df * loser.population
        
        winner.population -= self.casualties_win
        loser.population -= self.casualties_lose

    def outcome(self):
        if self.land1.cwi() > self.land2.cwi():
            self.winner = self.continent1
            self.loser = self.continent2
            self.land_won = self.land2
            self.calculate_casualties(self.land1, self.land2)
            
        elif self.land1.cwi() == self.land2.cwi():
            self.land1.population -= self.land1.population / 2
            self.land2.population -= self.land2.population / 2
        else:
            self.winner = self.continent2
            self.loser = self.continent1
            self.land_won = self.land1
            self.calculate_casualties(self.land2, self.land1)

class Civil_War:
    def __init__(self, land):
        self.continent = land.ruler
        self.land = land

        self.winner = None
        self.loser = None
        self.insurgents = 0
        self.government = 0
        self.casualties = 0

        self.land_won = None

        self.outcome()

    def calculate_casualties(self, winner, loser):
        df = loser / winner
        self.casualties = (1 - df) * df * self.land.population * 2
        self.land.population -= self.casualties

    def outcome(self):
        self.insurgents = self.land.cwi(2)
        self.government = self.land.cwi()
        if self.insurgents > self.government:
            self.winner = "Insurgents"
            self.loser = "Government"
            self.calculate_casualties(self.insurgents, self.government)
            self.continent.insurgent_land.append(self.land)
        elif self.insurgents == self.government: return
        else:
            self.winner = "Government"
            self.loser = "Insurgents"
            self.calculate_casualties(self.government, self.insurgents)

        self.continent.civil_casualties += self.casualties

    def __repr__(self):
        return f"Revolt in {self.land}\nInsurgents: {self.insurgents}\nGovernment: {self.government}\nWinner: {self.winner}\nLoser: {self.loser}\nCasualties: {self.casualties}\n"