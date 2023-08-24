#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .OGSExternal import OGSExternal
from .NetworkOGSExternal import NetworkOGSExternal
from .Merge import Merge

# Exclude folder from automatic documentation as OGS import causes trouble
__all__ = {'OGSExternal.runModel': False}
