#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class ResourceModel:
    """
    Parent class for all resource modules.
    """

    def getAbovegroundResources(self):
        """
        Get above-ground resource values
        Returns:
            vector with floats
        """
        return self.aboveground_resources

    def getBelowgroundResources(self):
        """
        Get below-ground resource values
        Returns:
            vector with floats
        """
        return self.belowground_resources

    def prepareNextTimeStep(self, t_ini, t_end):
        """
        Prepare next time step by initializing relevant variables.
        Args:
            t_ini (int): start of current time step in seconds
            t_end (int): end of current time step in seconds
        """
        pass

    def addPlant(self, plant):
        """
        Add each plant and its relevant geometry and parameters to the object to
        be used in the next time step.
        Args:
            plant (dict): tree object
        """
        pass

    def getInputParameters(self, **tags):
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
            print(arg)
            tag = arg.tag
            for i in range(0, len(required_tags)):
                if tag == required_tags[i]:
                    try:
                        super(ResourceModel, self).__setattr__(tag, float(arg.text))
                    except ValueError:
                        super(ResourceModel, self).__setattr__(tag, str(arg.text))
            try:
                required_tags.remove(tag)
            except ValueError:
                pass

            for i in range(0, len(optional_tags)):
                if tag == optional_tags[i]:
                    try:
                        super(ResourceModel, self).__setattr__(tag, float(arg.text))
                    except ValueError:
                        super(ResourceModel, self).__setattr__(tag, str(arg.text))

        if len(required_tags) > 0:
            string = ""
            for tag in required_tags:
                string += tag + " "
            raise KeyError(
                "Missing input parameters (in project file) for resource module initialisation: " + string)
