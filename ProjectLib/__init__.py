#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 15:25:03 2018

@author: bathmann
"""
#from XMLtoProject import XMLtoProject
if __name__ == '__main__' and __package__ is None:
    from XMLtoProject import XMLtoProject
    from Project import MangaProject
else:
    from .XMLtoProject import XMLtoProject
    from .Project import MangaProject