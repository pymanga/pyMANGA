#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sub-library of modules on plant mortality.


Mortality modules can be combined.
In this way, the survival of a plant is assessed on the basis of all the modules selected.
If at least one of the modules indicates the plant's death, the plant dies.

Example:
    ```xml
        <mortality>NoGrowth Random</mortality>
    ```
"""

from .Mortality import Mortality
