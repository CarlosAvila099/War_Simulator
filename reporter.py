from cProfile import label
import json
import matplotlib.pyplot as plt
import numpy as np

from pprint import pprint

def reporter(story, cont):
    results = json.load(open('Stories/Story' + str(story) + '.json', 'r'))

    days = np.arange(1, 31)

    income = np.array([])
    military = np.array([])
    population = np.array([])
    territory = np.array([])

    for day in days:
        population = np.append(population, results["Day " + str(day)][cont]["Population"])
        income = np.append(income, results["Day " + str(day)][cont]["Income"])
        territory = np.append(territory, results["Day " + str(day)][cont]["Territory"])
        military = np.append(military, results["Day " + str(day)][cont]["Military"])

    pprint(population)

    plt.title("Story 1") 
    plt.xlabel("Days") 
    plt.ylabel("Population") 
    plt.plot(days, population)
    plt.show()

    plt.title("Story 1") 
    plt.xlabel("Days") 
    plt.ylabel("Income") 
    plt.plot(days, income)
    plt.show()

    plt.title("Story 1") 
    plt.xlabel("Days") 
    plt.ylabel("Territory") 
    plt.plot(days, territory)
    plt.show()

    plt.title("Story 1") 
    plt.xlabel("Days") 
    plt.ylabel("Military") 
    plt.plot(days, military)
    plt.show()

reporter(1, "South America")