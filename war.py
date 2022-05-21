class War:
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