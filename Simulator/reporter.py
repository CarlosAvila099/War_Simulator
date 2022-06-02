from cProfile import label
import json
import matplotlib.pyplot as plt
import numpy as np

from pprint import pprint

def reporter(story, cont, dataset):
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

    data = {
        "Population": population,
        "Income": income,
        "Territory": territory,
        "Military": military
    }

    plt.title("Story " + str(story) + ": " + cont) 
    plt.xlabel("Days") 
    plt.ylabel(dataset) 
    plt.plot(days, data[dataset])
    plt.savefig('Graphs/Story ' + str(story) + '/' + cont + ' ' + dataset + '.png')
    plt.clf()

continents = ["North America", "South America", "Europe", "Africa", "Asia", "South-East Asia", "Oceania"]
parameters = ["Population", "Territory", "Military", "Income"]

#Story 1
for cont in continents:
    for par in parameters:
        reporter(1, cont, par)

#Story 2
for par in parameters:
    reporter(2, "Africa", par)
    
#Story 3
for par in parameters:
    reporter(3, "North America", par)
    reporter(3, "Asia", par)

#Story 4
for cont in continents:
    for par in parameters:
        reporter(4, cont, par)
        
#Story 5
for par in parameters:
    reporter(5, "Oceania", par)