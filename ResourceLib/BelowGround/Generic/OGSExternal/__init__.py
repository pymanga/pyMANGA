#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

from .OGSExternal import OGSExternal

# Exclude folder from automatic documentation as OGS import causes trouble
__all__ = {"OGSExternal.runModel": False}
