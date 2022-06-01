# Development Log
## Tasks
For this project, we were asked to represent a War Simulation through the use of python.
The principal parts of this project were:
* Data Analysis
* Simulator
    * Initialize
    * Growth Times
    * War Mechanics
    * Triggers
    * Conflict
    * Peace Times
    * Government Changes
* Data Creation
* Data Visualization

## Data Analysis

## Simulator
For this step of the project, we were given the task to create the simulator of the war using the information recovered from the previous step.

We started by analizing all the parts needed for the simulation to work, after this we started by making the classes needed and by setting specific constrainsts each class had. This helped us to avoid making big changes when encountering problems. Then we started to implement it in code, each part will be explained below.

### Initialize
For this part we needed to initialize the _Continents_ with certain properties:
* Territory
* Population
* Population Growth
* Income per Capita
* Literacy Rate
* Military Spend by % of GDP
* Government Rate

To solve this, we created a _Continent_ class with these properties, as well as some lists to keep track of the land, borders and neighbors each _Continent_ had.
We also created a _Land_ class to keep track of each peace of _Land_ a _Continent_ had.

### Growth Times
For this part of the simulation we needed to increase the poulation of each _Land_ every month, we created a _World_ class to keep track of each _Continent_ and the date of the simulation.
By advancing the simulation by a day, we advanced the _Continents_ and the _Lands_.

### War Mechanics
The war mechanics were simple, each _Continent_ will check for triggers and if a war started the order of evaluating which _Lands_ were to enter a war would be to left, right, top and bottom.

### Triggers
In this part, we needed to create the triggers to start either a _War_ or a _Civil War_.
There were two types of triggers:
* **Income:** When the total income of two neighboring _Continents_ reach a certain difference.
    * **Civil War:** When the difference is INCOME_THRESHOLD times the standard deviation of the world income.
    * **War:** When the difference is grater than one standard deviation of the world income.
* **Population:** When the density reaches one standard deviation above the average of the world populaiton.
    * **Civil War:** If the _Continent_ with a _Population Trigger_ is the poorest of his neighbors.
    * **War:** If the _Continent_ with a _Population Trigger_ has a neighbor poorer than him.

### Conflict
To determine the winner of a conflict, the _Capability of War Index_ (CWI) is calculated, it depends on the total income, government rate, literacy rate, military spending and a luck value.

As explained before, there can be two types of conflict, _Civil War_ or _War_.
* **Civil War:** It consists of two states.
    * **Random Walk:** In this state, the _Civil War_ has just begun, random lands are selected to see if an insurgent rise is made, this rise is decided by a 50% chance of happening, either it happens or not, that _Land_ is marked as visited and will not try another rising while in _Random Walk_. The _Random Walk_ ends when at least half of the _Lands_ are visited.
    If the _Random Walk_ has ended with at least one insurgent victory the _Civil War_ will continue, else it will be stopped.
    * **Insurgent Rise:** In this part, all the neighboring _Lands_ of an insurgent victory, will try an insurgent rise. This process is repeated until one of the following are met:
        * No more insurgent territories, the government has won, nothing changes.
        * The insurgents have occupied a certain percentage of the territory, 1/3 if the government rate is below 0.4 and 2/3 if the government rate if above 0.4. If this happens, a new government is selected with an extra INSURGENCY_SUPPORT value to the new government rate.
        * When the total casualties of the _Civil War_ are CASUALTY_STOP percentage of the population before the _Civil War_. If this happens, a new government is selected.
* **War:** A war between two _Continents_, each _Land_ neighboring the opposing _Continent_ will start a _Battle_ in the order mentioned in **War Mechanics**, the winner is selected and the _Land_ of the loser will be incorporated by the winner. The stop conditions are the following:
    * A _Continent_ has conquered 50% of the _Land_ of the opposing _Continent_, which will result in the _Continent_ annexing the losing _Continent_.
    * A _Continent_ has an income greater than 3 times the standard deviation of the opposing _Continent_, which will cause a complete cease fire in the loser _Continent_ and a new government will be selected.
    * There are STALE_TIME _Battles_ with a tie. Both _Continents_ will have a complete cease fire and select new governments.

Any type of conflict will be ended when:
* Any of the participating party has a complete cease fire.
* Any of the participating party is annexed by another _Continent_.

In this part, one problem we encountered was that _Continents_ that started any type of trigger will keep starting it, so we added a flag to check if any _Continent_ had started any type of war, if it had, that _Continent_ coulnd't start a war by the same trigger until the current war ended.

### Peace Times
This part of the simulation represents a _Continent's_ growth due to prosperity by not having any type of conflict through PEACE_TIME years.
To do this, we added a peace counter to each _Continent_, the counter was reset when any conflict involved the _Continent_.

### Government Changes
Besides the _Governmetn Changes_ made by conflicts, a new _Government Change_ happens every GOVERNMENT_TIME years.
To keep track of the information, we created a _Government Change_ class, that saves the date and the past and new government rates.

With all that made, we added a function to visualize in a grid all the _Continents_ thorugout the DURATION of the simulation.

## Data Creation
This step was to save the data made by the simulation and pass it to the **Data Visualization** step, to do this we opted to create a JSON file containing all the information the simulation had.
* First we tried to use the json library python had, it wouldn't work due to object having other objects inside.
* Then we tried to cast our object as a dict() to order the properties and then use json to give it the right format. It didn't work thantks to some classes containing _numpy.ndarray_, making it impossible to cast.
* At last, we tried by creating a to_json() function in each of our classes, it was time consuming and tiring, but it worked.
* Although the information is saved, it takes a lot of space, so we changed it to only saving the grid being shown.

## Data Visualization