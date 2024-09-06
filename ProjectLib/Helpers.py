import numpy as np


def string_to_function(expression):
    """
    Evaluate formula from project file
    Credits: https://saturncloud.io/blog/pythonnumpyscipy-converting-string-to-mathematical-function/#numpys-frompyfunc-function
    Args:
        expression (string): weighting formula (from prj file)
    Returns:
        array
    """
    def function(x, y):
        return eval(expression)

    return np.frompyfunc(function, 2, 1)