import random
from pprint import pprint
from continent import *

world = World(200,  [
                    Continent("Europe", 0, 0, 10530000, 750000000, 0.4, 22909.96, 98.59, 1.20, random.random()),
                    Continent("Asia", 11, 0, 32740000, 4030000000, 0.83, 7829.11, 96, 2.70, random.random())
                    ])

'''
Continent("South-East Asia", 0, 0, 11840000, 680000000, 1.14, 4523.84, 70, 2.70, random.random(), world)
Continent("North America", 0, 0, 24710000, 580000000, 1, 50984.45, 88, 3.4, random.random(), world)
Continent("Africa", 0, 0, 30272000, 1320000000, 2.45, 1969.69, 66.8, 1.76, random.random(), world)
Continent("South America", 0, 0, 17840000, 423000000, 1, 7692.31, 94.95, 5.08, random.random(), world)
Continent("Oceania", 0, 0, 8526000, 41000000, 1.4, 46209.11, 66, 2.10, random.random(), world)
'''

europe = world.continents[0]
#europe.civil_war(True, "Test")
asia = world.continents[1]
europe.war(True, asia, "Test")

while world.date < DURATION:
    world.advance()
#pprint(world.civil_wars)
pprint(world.wars)
pprint(world.govenment_changes)