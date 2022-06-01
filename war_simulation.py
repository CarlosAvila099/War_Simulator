import random
import copy
import matplotlib.pyplot as plt

from matplotlib import animation
from assets import json_array
from continent import World, Continent
from configuration import DURATION

world = World(50,  [
                    Continent("North America", 10, 5, 120, 24710000, 580000000, 1, 50984.45, 88, 3.4, random.random()),
                    Continent("South America", 26, 5, 180, 17840000, 423000000, 1, 7692.31, 94.95, 5.08, random.random()),
                    Continent("Europe", 19, 20, 30, 10530000, 750000000, 0.4, 22909.96, 98.59, 1.20, random.random()),
                    Continent("Africa", 30, 18, 150, 30272000, 1320000000, 2.45, 1969.69, 66.8, 1.76, random.random()),
                    Continent("Asia", 6, 30, 60, 32740000, 4030000000, 0.83, 7829.11, 96, 2.70, random.random()),
                    Continent("South-East Asia", 24, 36, 90, 11840000, 680000000, 1.14, 4523.84, 70, 2.70, random.random()),
                    Continent("Oceania", 36, 35, 210, 8526000, 41000000, 1.4, 46209.11, 66, 2.10, random.random()),
                    ])

history = []

def update_im(i, img, world: World):
    history.append(json_array(world.get_array()))
    world.advance()
    img.set_array(world.get_array())

fig, ax = plt.subplots()
img = ax.imshow(world.get_array())
ani = animation.FuncAnimation(fig, update_im, fargs=(img, world), frames=DURATION, repeat=False)
plt.show()

json = "["
for hist in history:
    json += f"[{hist}],"
json = json[:-1] + "]"

file = open("info.json", "w")
file.write(json)
file.close()