#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de, marie-christin.wimmler@tu-dresden.de
"""

import copy


class DynamicTimeStepping:

    def __init__(self, project):
        # Initialize concepts
        self.aboveground_resource_concept = project.getAbovegroundResourceConcept()
        self.belowground_resource_concept = project.getBelowgroundResourceConcept()
        self.plant_dynamic_concept = project.getPlantDynamicConcept()
        self.population_concept = project.getPopulationConcept()
        self.visualization_concept = project.getVisualizationConcept()
        self.visualization_concept.update(self.population_concept.getPlantGroups(), "Begin")
        ## Output configuration
        self.model_output_concept = project.getModelOutputConcept()

        # Arrays to store interim model results
        self.aboveground_resources = []
        self.belowground_resources = []
        self._previous_plant_groups = []

    ## This progresses one time step, by updating tree population and above-
    # and below-ground resources. Not all concepts have to be called with
    # the same frequency (i.e. only if update_x is true).
    def step(self, t_start, t_end, update_ag, update_bg):
        if update_ag:
            self.aboveground_resource_concept.prepareNextTimeStep(t_start, t_end)
        if update_bg:
            self.belowground_resource_concept.prepareNextTimeStep(t_start, t_end)
        self.plant_dynamic_concept.prepareNextTimeStep(t_start, t_end)
        plant_groups = self.population_concept.getPlantGroups()

        self.model_output_concept.writeOutput(plant_groups, t_start)
        # Initialize tree counter variable
        number_of_trees = 0
        for group_name, plant_group in plant_groups.items():
            for tree in plant_group.getPlants():
                number_of_trees += 1
                if update_ag:
                    self.aboveground_resource_concept.addPlant(tree)
                if update_bg:
                    self.belowground_resource_concept.addPlant(tree)
        # Only update resources if trees exist
        if number_of_trees > 0:
            if update_ag:
                self.aboveground_resource_concept.calculateAbovegroundResources()
                self.aboveground_resources = (
                    self.aboveground_resource_concept.getAbovegroundResources())
            if update_bg:
                self.belowground_resource_concept.calculateBelowgroundResources()
                self.belowground_resources = (
                    self.belowground_resource_concept.getBelowgroundResources())
        j = 0
        number_of_trees = 0
        eliminated_plant_groups = {}
        for group_name, plant_group in plant_groups.items():
            kill_indices = []
            for tree, i in zip(plant_group.getPlants(),
                               range(plant_group.getNumberOfPlants())):
                ## If a new tree is recruited in the current time step and
                # the respective resource was not updated, set survival of
                # the new tree to 1
                try:
                    ag = self.aboveground_resources[j]
                    bg = self.belowground_resources[j]
                    self.plant_dynamic_concept.progressTree(tree, ag, bg)
                except IndexError:
                    tree.setSurvival(1)

                if not tree.getSurvival():
                    kill_indices.append(i)

                j += 1

            # If all trees of a group died, make a copy of this tree set
            if len(kill_indices) > 0 and plant_group.getNRecruits() == 0:
                if len(kill_indices) == plant_group.getNumberOfPlants():
                    eliminated_plant_groups[plant_group.name] = copy.deepcopy(
                        plant_group)
                    self.model_output_concept.writeOutput(eliminated_plant_groups,
                                                 t_start,
                                                 group_died=True)
            plant_group.removePlantsAtIndices(kill_indices)
            plant_group.recruitPlants()

            # Add number of recruited trees to counter
            number_of_trees += plant_group.getNumberOfPlants()

        # Stop MANGA execution if no trees exist or were recruited
        if number_of_trees == 0:
            print("INFO: MANGA execution stopped because all trees died and "
                  "no new tree were recruited.")
            exit()
        self.visualization_concept.update(plant_groups, t_end)

    ## Last action, when timeloop is done
    def finish(self, time):
        self.visualization_concept.show(time)
        plant_groups = self.population_concept.getPlantGroups()
        # Write output in last time step, even if not defined in the project
        # file
        self.model_output_concept.writeOutput(plant_groups, time, force_output=True)

    def setResources(self, ag_resources, bg_resources):
        self.aboveground_resources = ag_resources
        self.belowground_resources = bg_resources

    def getResources(self):
        return [self.aboveground_resources, self.belowground_resources]
