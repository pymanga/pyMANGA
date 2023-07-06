#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .OGSLargeScale3DExternal import OGSLargeScale3DExternal
from .NetworkOGSLargeScale3DExternal import NetworkOGSLargeScale3DExternal


# Exclude folder from automatic documentation as OGS import causes trouble
__all__ = {'OGSLargeScale3DExternal.runModel': False}
