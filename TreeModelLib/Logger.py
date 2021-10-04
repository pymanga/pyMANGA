#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de

Adopted from: https://dev.to/duyixian1234/three-ways-to-automatically-add-functions-and-methods-calling-log-for-python-code-5fd0
"""

import logging
logger = logging.getLogger(__name__)


def method_logger(method):
    def inner(self, *args, **kwargs):
        ret = method(self, *args, **kwargs)
        module = method.__module__.split(".")
        logger.info(module[-1] + ': ' + method.__name__ + ', self: ' +
                    str(self))
        return ret
    return inner


'''
The function and class below provide a method to logg all calls (but only 
the first level of their occurrence, i.e. without inheritance).

Change required in TreeModel to: 

    from .Logger import MethodLogger
    class TreeModel(MethodLogger):
'''


def method_logger_x(method, obj):
    def inner(*args, **kwargs):
        ret = method(*args, **kwargs)
        #logger.info(f'Call method {method.__name__} of {obj} with
        # {args, kwargs} returns {ret}')
        module = method.__module__.split(".")
        logger.info(module[1] + '.' + module[-1] + ': ' + method.__name__)
        return ret
    return inner


class MethodLogger:
    def __getattribute__(self, key):
        value = super().__getattribute__(key)
        if callable(value) and not key.startswith('__'):
            return method_logger_x(value, self)
        return value


'''
Other option: manual assignment of logging prints

Add the following function to TreeModel and add the following statement to 
each method that should be logged

self.setLoggingInfo(type(self).__name__, sys._getframe().f_code.co_name)
'''


def setLoggingInfo(self, class_name, method_name):
    # class_name: type(self).__name__
    # method_name: sys._getframe().f_code.co_name
    return logging.info(str(class_name) + ": " + str(method_name))

