#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""

import numpy as np
from PlantModelLib.Mortality.Random import Random


class RandomGrowth(Random):

    def __init__(self, args, case):
        super(Random, self).__init__(args, case)
        # Read input parameters from xml file
        self.getInputParameters(args)
        # Default values if no inputs are given
        try:
            self._k_die
        except:
            # Calibration factor default: 1e-12
            self._k_die = 1e-12
            print("NOTE: Use default `probability`: " + str(self._k_die) + ".")

    def setSurvive(self, args): #getSurvival
        self._survive = 1
        # Calculate the probability to die
        args.delta_volume = args.volume - args.volume_before

        # = dV/dt/V
        relative_volume_increment = args.delta_volume / (args.time *
                                                         args.volume)
        p_die = self._k_die / relative_volume_increment

        # Get a random number
        r = np.random.uniform(0, 1, 1)
        if r < p_die:
            self._survive = 0
            print("\t Tree died (RandomGrowth).")

    def getSurvive(self):
        return self._survive

    def setMortalityVariables(self, args, growth_concept_information):
        # Variable to store volume of previous time step (m³)
        try:
            args.volume_before = growth_concept_information[
                "volume_previous_ts"]

            if args.volume_before == "NaN":
                args.volume_before = 0
        except KeyError:
            args.volume_before = 0

    def getMortalityVariables(self, args, growth_concept_information):
        # The current tree volume is the volume of t-1 in the next time step
        growth_concept_information["volume_previous_ts"] = \
            args.volume
        return growth_concept_information

    def getInputParameters(self, args):
        # All tags are optional
        missing_tags = ["type", "mortality", "k_die"]
        for arg in args.iterdescendants():
            tag = arg.tag
            if tag == "k_die":
                self._k_die = float(args.find("k_die").text)
            elif tag == "type":
                case = args.find("type").text
            try:
                missing_tags.remove(tag)
            except ValueError:
                print("WARNING: Tag " + tag + " not specified for " +
                      super().getConceptName() + " (" + case + ") " +
                      "mortality initialisation!")
