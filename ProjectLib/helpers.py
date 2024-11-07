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
    self.x_1, self.x_2 = x1, x2
    self.y_1, self.y_2 = y1, y2

    self.l_x = self.x_2 - self.x_1
    self.l_y = self.y_2 - self.y_1
