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

    def getInputParameters(self, args, required_tags=None, optional_tags=None, lib="resource"):
        """
        Read module tags from project file.
        Args:
            args (lxml.etree._Element): module specifications from project file tags
            required_tags (array): list of tags that need to be read from the project file
            optional_tags (array): list of tags that can be specified in the project file
            lib (string): name of library
        """

        if optional_tags is None:
            optional_tags = []
        if required_tags is None:
            required_tags = []
        for arg in args.iterdescendants():
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
                "Missing input parameters (in project file) for " + lib + " module initialisation: " + string)
