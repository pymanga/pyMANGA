This is the abstract class of the ```pyMANGA.ResourceLib```.

# Information for developers 
## Structure of each Resource module

Each resource module must contain the following methods:

- ``prepareNextTimeStep(self, t_ini, t_end)``: Prepares next time step by initializing relevant variables.
- ``addPlant(self, plant)``: Adds each plant and its relevant geometry and parameters to the object to be used in the next time step.
- One of: ``calculateAbovegroundResources(self)`` or ``calculateBelowgroundResources(self)``: Calculates and sets the resource factor of each plant.

## ResourceModel

This class contains getter functions which are accessed by ``pyMANGA.TimeLoopLib``.

### getAbovegroundResources

Returns a list of length = number of plants indicating the above-ground resource availability of each plant.

### getBelowgroundResources

Returns a list of length = number of plants indicating the below-ground resource availability of each plant.

### superordinate methods

This library also contains superordinate functions that can be used by all resource moduls such as:

#### getInputParameters

Reads and processes the specifications provided in the project file relevant for the chosen resource module.

The ``tags`` dictionary supports the following keys:

- ``prj_file``: XML element containing module parameters
- ``required``: list of required tag names
- ``optional``: list of optional tag names
- ``case_insensitive``: (optional) list of tag names whose string values should be converted to lowercase. Tags not in this list preserve their original case. Use this for enum-like parameters (e.g. ``backend_type``) but not for file paths.

#### makeGrid

Create a regular grid that extends a rectangle of size x*y, where
```python
x = x_2 - x_1
y = y_2 - y_1
```
and the size of each cell is
````python
xs = x / x_resolution
ys = y / y_resolution
````

Additionally, ``makeGrid`` stores the domain dimensions (``_lx``, ``_ly``) and reads the
optional ``periodic_boundary`` flag (set once at the ``<resources>`` level, see below).
If ``periodic_boundary`` is True, distance calculations can use the minimum image convention
via ``wrapDistance``.

## Periodic boundary conditions

Periodic boundary conditions (PBC) are configured **once** at the ``<resources>`` level and
apply to both above- and below-ground modules. Specifying ``<periodic_boundary>`` inside
``<aboveground>`` or ``<belowground>`` raises an error.

```xml
<resources>
    <periodic_boundary> True </periodic_boundary>
    <aboveground>
        <type> Default </type>
    </aboveground>
    <belowground>
        <type> SymmetricZOI </type>
        <domain> ... </domain>
    </belowground>
</resources>
```

When enabled, distance calculations in supported modules (``AsymmetricZOI``,
``SymmetricZOI``, ``FON``, ``SaltFeedbackBucket``) use the minimum image convention
via ``wrapDistance``. The above- and below-ground domains must share the same extent.

#### wrapDistance

Apply the minimum image convention for periodic boundary conditions.
Given distance components ``dx`` and ``dy`` (scalar or array), returns the wrapped values
corresponding to the shortest distance across periodic images.

This method is a no-op when ``periodic_boundary`` is False.

Modules that compute plant-to-grid or plant-to-plant distances should call this method
to support periodic boundaries transparently:

```python
dx, dy = self.wrapDistance(dx, dy)
distance = (dx**2 + dy**2)**0.5
```

---

