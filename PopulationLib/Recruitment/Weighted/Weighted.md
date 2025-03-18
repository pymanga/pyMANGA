# Description

Recruitment module that defines the location new plants.

Recruitment of new plants is based on a weight map.

The size (geometry) and attributes of a plant are taken from the species file (see ``pyMANGA.PopulationLib.Species``).

# Usage

```xml
<distribution>
    <type> Weighted </type>
    <weight_file> path/to/weights.csv </weight_file>
</distribution>
```

# Attributes

- ``type`` (string): "Random"
- ``weight_file`` (str): Path to weight map (i.e., provided as csv file with the following columns: x-coordinate, y-coordinate, weight)

# Value

see ``pyMANGA.PopulationLib.Recruitment``

# Details
## Purpose

Define whether a plant can establish at a certain location based on a weight map.
Weights should be provided as value between 0 and 1, whereby 1 indicates high chances for establishment in this cell, and 0 indicates no chance.

## Process overview

- *readWeightsFile*: get weights from csv file
- *getPositions*: determine plant positions based on weights

## Sub-processes
### readWeightsFile

The wights map must describe a regular grid.
The file must be a csv file with the following columns: x-coordinate, y-coordinate, weight.
The coordinates are the coordinates of the grid centers.
Weights should be given as a value between 0 and 1, where 1 indicates a high chance of establishment in that cell and 0 indicates no chance.

Columns of the csv-file can be separated by: ";|,|\t".

**Note** 
- Make sure the boundaries of the weight map match that of the model.
- Make sure weights are > 0.

### getPositions

Location (xy) of new plants is drawn from a weighted uniform distribution.

The probability of each grid cell (`r`) is calculated based on the weights with

``python
r = np.random.random(no_cells) ** (1 / weights)
``

The resulting vector (`r`) is sorted and the first N cells are selected, where N is the number of plants recruited in the current time step.
The location (xy) of the plants is than randomly chosen within the selected grid cells.

## Application & Restrictions

-

# References

-

# Author(s)

Marie-Christin Wimmler


# See Also

``pyMANGA.PopulationLib.Recruitment``,
``pyMANGA.PopulationLib.Species``



