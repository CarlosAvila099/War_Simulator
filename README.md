# War_Simulator
Final Project of Simulation Class, a simulator of war between continents.

## Specification
Python 3.9.7

## Libraries used
* numpy
* matplotlib

If any library causes an error, run the command _pip install_.

## Usage
To run the simulator download all the files, change **configuration.py** as you desire and run **war_simulation.py**. Take into account that the simulator can be run in two different ways.

### Simulation
This part runs the simulation while representing conflicts and growth, it also contains a visualization.
To run it in this form, the _RUN_ flag in **configuration.py** must be _True_.

### Story Reporting
This part runs the simulation without any way to keep track of wars or visualization, it is used to create data for stories.
To run it in this form, the _RUN_ flag in **configuration.py** must be _False_.

### Modifying Data
* To modify data you can modify **configuration.py** to modify behaviour of the conflicts, growth and duration of certain aspects of the simulator.
* To modify _Continent_ information, modify, add or remove _Continents_ from the array given to _World_ in **war_simulation.py**.