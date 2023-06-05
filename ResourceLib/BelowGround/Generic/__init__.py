#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 15:25:03 2018

@author: bathmann
"""

from .OGSLargeScale3DExternal import OGSLargeScale3DExternal
from .NetworkOGSLargeScale3DExternal import NetworkOGSLargeScale3DExternal


# Exclude folder from automatic documentation as OGS import causes trouble
__pdoc__ = {'OGSLargeScale3DExternal.runModel': False}
