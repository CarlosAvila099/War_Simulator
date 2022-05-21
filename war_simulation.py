import random
from pprint import pprint
from continent import *

world = World(200)

europe = Continent("Europe", 10530000, 750000000, 0.4, 22909.96, 98.59, 1.20, random.random(), world)
'''
asia = Continent("Asia", 32740000, 4030000000, 0.83, 7829.11, 96, 2.70, random.random(), world)
seasia = Continent("South-East Asia", 11840000, 680000000, 1.14, 4523.84, 70, 2.70, random.random(), world)
namerica = Continent("North America", 24710000, 580000000, 1, 50984.45, 88, 3.4, random.random(), world)
africa = Continent("Africa", 30272000, 1320000000, 2.45, 1969.69, 66.8, 1.76, random.random(), world)
samerica = Continent("South America", 17840000, 423000000, 1, 7692.31, 94.95, 5.08, random.random(), world)
oceania = Continent("Oceania", 8526000, 41000000, 1.4, 46209.11, 66, 2.10, random.random(), world)
'''
world.continents = [europe]

months = 0      # Is reset when GROWTH_TIME months have passed.

europe.civil_war(True)
while world.date < DURATION:
    world.advance()
pprint(world.civil_wars)
print(world.govenment_changes)