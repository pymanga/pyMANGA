# Description

Dispersal module that defines the location new plants based on the parents position.

New plants are randomly distributed around the parent tree.
The probability density function is defined by the user.

The size (geometry) and attributes of a plant are taken from the species file (see ``pyMANGA.PopulationLib.Species``).

# Usage

```xml
<dispersal>
    <type> Distance2Parent </type>
    <distribution>normal</distribution>
    <scale>0.5</scale>
    <loc>0</loc>
</dispersal>
```

# Attributes

- ``type`` (string): "Random"
- ``distribution`` (str): probability density function, i.e., 'normal', 'uniform', 'exponential'. See [numpy random generator](https://numpy.org/doc/stable/reference/random/legacy.html) for specification.

# Value

see ``pyMANGA.PopulationLib.Dispersal``

# Details
## Purpose

Define the location of new plants added to the model based on the position of the parent plant.

## Process overview
#### getPositions

The position of new seedlings is calculated depending on the parent plant (`xp`, `yp`).
Therefore, the distance between the parent and `N` its seedlings is calculated based on a probability density function (``getDistances``).
Based on the distance (`dist2parent`) the seedlings are randomly distributed around the plant by generating a random ``angle`` (uniform distribution) and using 

``python
angle = np.random.uniform(low=0, high=2 * np.pi, size=N)
x_new = xp + dist2parent * np.sin(angle)
y_new = yp + dist2parent * np.cos(angle)
``

#### getDistances

The distance between the parent plant and seedlings is based on a probability density function using the [numpy random generator](https://numpy.org/doc/stable/reference/random/legacy.html).
Therefore, N random numbers are drawn from the chosen distribution, where N is the number of new seedlings produced by the each plant.

N is determined in ``pyMANGA.PopulationLib.Production``.

## Application & Restrictions

- This module needs seed production per individual (see ``pyMANGA.PopulationLib.Production``).

# References

-

# Author(s)

Marie-Christin Wimmler


# See Also

``pyMANGA.PopulationLib.Production``,
``pyMANGA.PopulationLib.Dispersal``,
``pyMANGA.PopulationLib.Species``

# Examples
The seeds of a tree can, for example, be distributed uniformly within a radius of up to 20 meters (high) or exponentially with a scale factor of 0.5 (scale), so that most seeds land close to the parent tree.
````xml
<dispersal>
    <type> Distance2Parent </type>
    <distribution> uniform </distribution>
    <high> 20 </high>
</dispersal>
or
<dispersal>
    <type> Distance2Parent </type>
    <distribution>exponential</distribution>
    <scale>0.5</scale>
</dispersal>
````
