import numpy as np


def getInputParameters(myself, **tags):
    """
    Read module tags from project file.
    Args:
        tags (dict): dictionary containing tags found in the project file as well as required and optional tags of
        the module under consideration.
    """
    try:
        prj_file_tags = tags["prj_file"]
    except KeyError:
        prj_file_tags = []
        print("WARNING: Module attributes are missing.")
    try:
        required_tags = tags["required"]
    except KeyError:
        required_tags = []
    try:
        optional_tags = tags["optional"]
    except KeyError:
        optional_tags = []

    for arg in prj_file_tags.iterdescendants():
        tag = arg.tag
        for i in range(0, len(required_tags)):
            if tag == required_tags[i]:
                try:
                    myself.__setattr__(tag, float(eval(arg.text)))
                except (ValueError, NameError, SyntaxError):
                    myself.__setattr__(tag, str(arg.text))
        try:
            required_tags.remove(tag)
        except ValueError:
            pass

        for i in range(0, len(optional_tags)):
            if tag == optional_tags[i]:
                try:
                    myself.__setattr__(tag, float(eval(arg.text)))
                except (ValueError, NameError, SyntaxError):
                    myself.__setattr__(tag, str(arg.text))

    if len(required_tags) > 0:
        string = ""
        for tag in required_tags:
            string += tag + " "
        raise KeyError(
            "Missing input parameters (in project file) for resource module initialisation: " + string)


def setModelDomain(self, x1, x2, y1, y2):
    """
    Adds model domain boundaries to the object.
    Args:
        x1 (float): x-coordinate of left bottom border of grid
        x2 (float): x-coordinate of right bottom border of grid
        y1 (float): y-coordinate of left top border of grid
        y2 (float): y-coordinate of right top border of grid
    """
    self.x_1, self.x_2 = x1, x2
    self.y_1, self.y_2 = y1, y2

    self.l_x = self.x_2 - self.x_1
    self.l_y = self.y_2 - self.y_1


def string_to_function(self, expression):
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
