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
