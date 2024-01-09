#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. include:: ./OGSExternal.md
"""

from .OGSExternal import OGSExternal

# Exclude folder from automatic documentation as OGS import causes trouble
__all__ = {"OGSExternal.runModel": False}
