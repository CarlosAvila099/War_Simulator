from copy import deepcopy
import random
import matplotlib.pyplot as plt

from matplotlib import animation
from assets import Story_Continent, json_array
from continent import World, Continent
from configuration import DURATION, STORY_SET

from pprint import pprint


# STORY 1: NORMAL WORLD (Geographically acurrate. Normal data, without changes)
world = World(85,  [
                        Continent("North America", 5, 7, 30, 24710000, 580000000, 1, 50984.45, 88, 3.4, random.random()),
                        Continent("South America", 5, 30, 60, 17840000, 423000000, 1, 7692.31, 94.95, 5.08, random.random()),
                        Continent("Europe", 27, 23, 90, 10530000, 750000000, 0.4, 22909.96, 98.59, 1.20, random.random()),
                        Continent("Africa", 23, 42, 120, 30272000, 1320000000, 2.45, 1969.69, 66.8, 1.76, random.random()),
                        Continent("Asia", 41, 15, 150, 32740000, 4030000000, 0.83, 7829.11, 96, 2.70, random.random()),
                        Continent("South-East Asia", 60, 41, 180, 11840000, 680000000, 1.14, 4523.84, 70, 2.70, random.random()),
                        Continent("Oceania", 68, 57, 210, 8526000, 41000000, 1.4, 46209.11, 66, 2.10, random.random()),
                    ])

'''
# STORY 2: AFRICA CENTER (All around Africa. Increase in Income and Military Spend of As [1969.69 --> 12354.2][1.76 --> 6.76])
#  - Values are adjusted so that NA and As can go to war with Af, Af can't defend itself from them, but Af can attack the other continents. 
world = World(85,  [
                    Continent("North America", 16, 11, 30, 24710000, 580000000, 1, 50984.45, 88, 3.4, random.random()),
                    Continent("South America", 13, 48, 60, 17840000, 423000000, 1, 7692.31, 94.95, 5.08, random.random()),
                    Continent("Europe", 50, 58, 90, 10530000, 750000000, 0.4, 22909.96, 98.59, 1.20, random.random()),
                    Continent("Africa", 31, 33, 120, 30272000, 1320000000, 2.45, 12354.2, 66.8, 6.76, random.random()),
                    Continent("Asia", 50, 6, 150, 32740000, 4030000000, 0.83, 7829.11, 96, 2.70, random.random()),
                    Continent("South-East Asia", 55, 38, 180, 11840000, 680000000, 1.14, 4523.84, 70, 2.70, random.random()),
                    Continent("Oceania", 33, 59, 210, 8526000, 41000000, 1.4, 46209.11, 66, 2.10, random.random()),
                    ])
'''
'''
# STORY 3: COLD WAR 2 (Geographically accurate. NA, SA, Eu, S-EA and O against As and Af. )
#  - Increase Military Spend in As, Af and NA; increase Income in SA, Eu, S-EA and O; half overall Growth)
#  - ([3.4 --> 12.4][1.76 --> 4.76][2.70 --> 9.70]; 
#     [7692.31 --> 17692.31][22909.96 --> 62909.96][4523.84 --> 34723.84][46209.11 --> 86209.11];
#     [half in every continent])
world = World(85,  [
                    Continent("North America", 5, 7, 30, 24710000, 580000000, 0.5, 50984.45, 88, 12.4, random.random()),
                    Continent("South America", 5, 30, 60, 17840000, 423000000, 0.5, 17692.31, 94.95, 5.08, random.random()),
                    Continent("Europe", 27, 23, 90, 10530000, 750000000, 0.2, 62909.96, 98.59, 1.20, random.random()),
                    Continent("Africa", 23, 42, 120, 30272000, 1320000000, 1.22, 1969.69, 66.8, 4.76, random.random()),
                    Continent("Asia", 41, 15, 150, 32740000, 4030000000, 0.4, 7829.11, 96, 9.70, random.random()),
                    Continent("South-East Asia", 60, 41, 180, 11840000, 680000000, 0.6, 34723.84, 70, 2.70, random.random()),
                    Continent("Oceania", 68, 57, 210, 8526000, 41000000, 0.7, 86209.11, 66, 2.10, random.random()),
                    ])
'''
'''
# STORY 4: SWITCH OF POWER (New arrangement of continents. The Income of NA and As goes down, while Income of SA, Eu and S-EA goes up). 
#  - ([50984.45 --> 10984.45][7829.11 --> 1829.11]; [7692.31 --> 53692.31][22909.96 --> 35909.96][4523.84 --> 28523.84])
world = World(85,  [
                    Continent("North America", 22, 14, 30, 24710000, 580000000, 1, 10984.45, 88, 3.4, random.random()),
                    Continent("South America", 4, 35, 60, 17840000, 423000000, 1, 53692.31, 94.95, 5.08, random.random()),
                    Continent("Europe", 30, 37, 90, 10530000, 750000000, 0.4, 35909.96, 98.59, 1.20, random.random()),
                    Continent("Africa", 19, 54, 120, 30272000, 1320000000, 2.45, 1969.69, 66.8, 1.76, random.random()),
                    Continent("Asia", 44, 14, 150, 32740000, 4030000000, 0.83, 1829.11, 96, 2.70, random.random()),
                    Continent("South-East Asia", 67, 40, 180, 11840000, 680000000, 1.14, 28523.84, 70, 2.70, random.random()),
                    Continent("Oceania", 61, 56, 210, 8526000, 41000000, 1.4, 46209.11, 66, 2.10, random.random()),
                    ])
'''
'''
# STORY 5: OCEANIA CONQUEST (Geographically acurrate. Increase Growth, Income and Military Spend in O 
#   - [1.4 --> 8.4][46209.11 --> 356209.11][2.10 --> 102.10])
world = World(85,  [
                    Continent("North America", 5, 7, 30, 24710000, 580000000, 1, 50984.45, 88, 3.4, random.random()),
                    Continent("South America", 5, 30, 60, 17840000, 423000000, 1, 7692.31, 94.95, 5.08, random.random()),
                    Continent("Europe", 27, 23, 90, 10530000, 750000000, 0.4, 22909.96, 98.59, 1.20, random.random()),
                    Continent("Africa", 23, 42, 120, 30272000, 1320000000, 2.45, 1969.69, 66.8, 1.76, random.random()),
                    Continent("Asia", 41, 15, 150, 32740000, 4030000000, 0.83, 7829.11, 96, 2.70, random.random()),
                    Continent("South-East Asia", 60, 41, 180, 11840000, 680000000, 1.14, 4523.84, 70, 2.70, random.random()),
                    Continent("Oceania", 68, 57, 210, 8526000, 41000000, 8.4, 356209.11, 98, 102.10, random.random()),
                    ])
'''
def update_im(i, img, world: World):
    history.append(json_array(world.get_array()))
    world.advance()
    img.set_array(world.get_array())

show = False

if show:
    history = []
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
else:
    runs = [deepcopy(world) for x in range(STORY_SET)]

    average = Story_Continent("Average")
    continents = {
        "North America": Story_Continent("North America"),
        "South America": Story_Continent("South America"),
        "Europe": Story_Continent("Europe"),
        "Africa": Story_Continent("Africa"),
        "Asia": Story_Continent("Asia"),
        "South-East Asia": Story_Continent("South-East Asia"),
        "Oceania": Story_Continent("Oceanias")
    }
    
    for x in range(DURATION):
        print(f"Simulating Day {x+1}/{DURATION}")
        average.add_day()
        for cont in continents.keys(): continents[cont].add_day()

        for num, run in enumerate(runs):
            print(f"\tRunning World {num+1}/{STORY_SET}")
            run.advance()

            avg = run.get_info()
            for cont in continents.keys(): 
                if cont in avg.keys(): continents[cont].add_info(avg[cont])

        for cont in continents.keys(): 
            continents[cont].end_day()
            average.add_continent(continents[cont])
        average.end_day()

    general = average.get_average()
    text = (
        "Story:\n"
        "\tGeneral:\n"
        f"\t\tPopulation: {general['population']}\n"
        f"\t\tTerritory: {general['territory']}\n"
        f"\t\tMilitary: {general['military']}\n"
        f"\t\tIncome: {general['income']}\n"
    )
    for cont in continents.keys():
        continent = continents[cont].get_average()
        text += (
            f"\t{cont}:\n"
            f"\t\tPopulation: {continent['population']}\n"
            f"\t\tTerritory: {continent['territory']}\n"
            f"\t\tMilitary: {continent['military']}\n"
            f"\t\tIncome: {continent['income']}\n"
        )

    for day in range(DURATION):
        text += (
            f"Day {day+1}:\n"
            "\tGeneral:\n"
            f"\t\tPopulation: {average.population[day]}\n"
            f"\t\tTerritory: {average.territory[day]}\n"
            f"\t\tMilitary: {average.military[day]}\n"
            f"\t\tIncome: {average.income[day]}\n"
        )
        for cont in continents.keys():
            continent = continents[cont]
            text += (
                f"\t{cont}:\n"
                f"\t\tPopulation: {continent.population[day]}\n"
                f"\t\tTerritory: {continent.territory[day]}\n"
                f"\t\tMilitary: {continent.military[day]}\n"
                f"\t\tIncome: {continent.income[day]}\n"
            )
    
    file = open("Stories/Story1.txt", "w")
    file.write(text)
    file.close()