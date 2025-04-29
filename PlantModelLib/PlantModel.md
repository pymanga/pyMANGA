This is the abstract class of the ```pyMANGA.PlantModelLib```.

# Information for developers 
## Structure of each PlantModel module

Each plant model module must contain the following methods:

- ``prepareNextTimeStep(self, t_ini, t_end)``: Prepares next time step by initializing relevant variables.
- ``progressPlant(self, tree, aboveground_resources, belowground_resources):``: Manages growth procedures for a timestep --- read tree geometry and parameters, schedule computations, and update tree geometry and survival

Each mortality module must contain the following methods:

- ``getSurvice(self, plant_module)``: Determine if plant survives based on annual probability to reach maximum age. Set attribute survival variable to 0 if plant died. Default  is 1 if plant lived
- ``setSurvive(self)``: Get survival status of a plant.

Mortality modules are initialized and invoked within the plant model.

## PlantModel

This class contains getter and setter functions which necessary for the mortality modules


---




