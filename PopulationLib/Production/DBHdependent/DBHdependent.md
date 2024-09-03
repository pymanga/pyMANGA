# Description

This module calculates dbh-dependent seed production using a log-linear equation.


See <a href="https://doi.org/10.1002/jwmg.291" target="_blank">Rose et al. (2011)</a> for prediction models for common oak species.

# Usage

```xml
<production>
    <type> DBHdependent </type>
    <formula>0.279 + 0.01152*x</formula>
    <production_nth_timestep> 2 </production_nth_timestep>
</production>
```

# Attributes

- ``type`` (string): "DBHdependent" (no other values accepted)
- ``formula`` (string): equation of type log10(Y) ~ X, where X is the dbh and Y the number of seeds produced by a plant
- ``production_nth_timestep`` (int): production period given as n-th timestep.

# Value

An integer indicating the total number of seed produced in the model domain.

# Details
## Purpose

## Process overview

## Sub-processes

## Application & Restrictions

- The number of new seeds increases exponentially if no limiting factor (e.g., competition, mortality) is activated

# References

<a href="https://doi.org/10.1002/jwmg.291" target="_blank">Rose et al. (2011)</a>

# Author(s)

Marie-Christin Wimmler, Chris Wudel

# See Also

# Examples


