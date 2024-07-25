Library of **above**- and **below**-ground resource modules.

Each module returns a list of values indicating the availability of below-ground resources for each plant.
The value ranges between 0 and 1, with 0 indicating no resource availability and 1 full resource availability (i.e., no limitation).

This library also contains **superordinate functions** that can be used by all resource moduls.


### makeGrid

Create a regular grid that extends a rectangle of size x*y, where
```python
x = x_2 - x_1
y = y_2 - y_1
```
and the size of each cell is
and cell size of
````python
xs = x_2 / x_resolution
ys = y_2 / y_resolution
````

