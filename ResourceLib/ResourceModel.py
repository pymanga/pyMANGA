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

    def getInputParameters(self, args, missing_tags=[]):
        """
        Read module tags from project file.
        Args:
            args (lxml.etree._Element): module specifications from project file tags
            missing_tags (array): list of tags that need to be read from the project file
        """

        for arg in args.iterdescendants():
            tag = arg.tag
            for i in range(0, len(missing_tags)):
                if tag == missing_tags[i]:
                    try:
                        super(ResourceModel, self).__setattr__(tag, float(arg.text))
                    except ValueError:
                        super(ResourceModel, self).__setattr__(tag, str(arg.text))
            try:
                missing_tags.remove(tag)
            except ValueError:
                pass

        if len(missing_tags) > 0:
            string = ""
            for tag in missing_tags:
                string += tag + " "
            raise KeyError(
                "Tag(s) " + string +
                "are not specified for resource module initialisation " +
                "in project file.")
