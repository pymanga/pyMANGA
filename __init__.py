#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PYthon Models for AGeNt-based resource GAthering (pyMANGA) is a collection of models describing vegetation population dynamics from first principles.
pyMANGA is modular, and descriptions of individual tree growth, resource availability and competition dynamics can be quickly interchanged.

The documentation of a module consists of the following parts
1. module description
2. specification of tags to be used in the pyMANGA project file (if applicable)
3. source code documentation.

*Note*
All parameters are defined in SI units unless indicated otherwise.

For general information about the pyMANGA project and tutorials visit our website: http://pymanga.forst.tu-dresden.de/

CoreTeam:
    @[jbathmann](https://github.com/jbathmann)
    @[mcwimm](https://github.com/mcwimm/)
    @[jvollhueter](https://github.com/jvollhueter)
"""
import os, sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Define docstring type for documentation rendering with pdoc
__docformat__ = "google"
