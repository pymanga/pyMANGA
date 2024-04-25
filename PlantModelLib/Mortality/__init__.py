#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sub-library of modules on plant mortality.

This page contains the documentation for the mortality modules.
All mortality modules can be combined.
In this way, the survival of a plant is assessed on the basis of all selected modules.
If at least one of the modules indicates the death of the plant, the plant dies.
To select multiple mortality modules, list the names of the modules separated by commas in the mortality tag.
You must also add the attributes of the selected modules.
For information about these attributes, see the pages for each module.

Example:
    ```xml
        <mortality>NoGrowth Random</mortality>
    ```
"""

from .Mortality import Mortality
