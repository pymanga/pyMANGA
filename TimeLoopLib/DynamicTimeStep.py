#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de, marie-christin.wimmler@tu-dresden.de
"""

import copy


class DynamicTimeStep:
    def __init__(self, project):
        """
        Manage time steps.
        Sets modules, i.e., resources, plant, population, output and visualization
        Args:
            project: project object
        """
        # Initialize concepts
        self.aboveground_resource_concept = project.getAbovegroundResourceConcept()
        self.belowground_resource_concept = project.getBelowgroundResourceConcept()
        # self.plant_dynamic_concept = project.getPlantDynamicConcept()
        self.population_concept = project.getPopulationConcept()
        self.visualization_concept = project.getVisualizationConcept()
        self.visualization_concept.update(self.population_concept.getPlantGroups(), "Begin")
        ## Output configuration
        self.model_output_concept = project.getModelOutputConcept()

        # Arrays to store interim model results
        self.aboveground_resources = []
        self.belowground_resources = []
        self._previous_plant_groups = []

    def step(self, t_start, t_end, update_ag, update_bg):
        """
        Define time step.
        Progresses model by one step, i.e., updates resources and plant population.
        Args:
            t_start (float): start of time step
            t_end (float): end of time step
            update_ag (bool): indicate whether above-ground module is called within the current time step
            update_bg (bool): indicate whether below-ground module is called within the current time step
        """
        if update_ag:
            self.aboveground_resource_concept.prepareNextTimeStep(t_start, t_end)
        if update_bg:
            self.belowground_resource_concept.prepareNextTimeStep(t_start, t_end)
        plant_groups = self.population_concept.getPlantGroups()

        self.model_output_concept.writeOutput(plant_groups, t_start)
        # Initialize plant counter variable
        number_of_plants = 0
        for group_name, plant_group in plant_groups.items():
            for plant in plant_group.getPlants():
                plant.plant_dynamic_concept.prepareNextTimeStep(t_start, t_end)
                number_of_plants += 1
                if update_ag:
                    self.aboveground_resource_concept.addPlant(plant)
                if update_bg:
                    self.belowground_resource_concept.addPlant(plant)
        # Only update resources if plants exist
        if number_of_plants > 0:
            if update_ag:
                self.aboveground_resource_concept.calculateAbovegroundResources()
                self.aboveground_resources = (
                    self.aboveground_resource_concept.getAbovegroundResources())
            if update_bg:
                self.belowground_resource_concept.calculateBelowgroundResources()
                self.belowground_resources = (
                    self.belowground_resource_concept.getBelowgroundResources())
        j = 0
        number_of_plants = 0
        eliminated_plant_groups = {}
        for group_name, plant_group in plant_groups.items():
            kill_indices = []
            for plant, i in zip(plant_group.getPlants(),
                               range(plant_group.getNumberOfPlants())):
                ## If a new plant is recruited in the current time step and
                # the respective resource was not updated, set survival of
                # the new plant to 1
                try:
                    ag = self.aboveground_resources[j]
                    bg = self.belowground_resources[j]
                    plant.plant_dynamic_concept.progressPlant(plant, ag, bg)
                except IndexError:
                    plant.setSurvival(1)

                if not plant.getSurvival():
                    kill_indices.append(i)

                j += 1

            # If all plants of a group died, make a copy of this plant set
            if len(kill_indices) > 0 and plant_group.getNRecruits() == 0:
                if len(kill_indices) == plant_group.getNumberOfPlants():
                    eliminated_plant_groups[plant_group.name] = copy.deepcopy(
                        plant_group)
                    self.model_output_concept.writeOutput(eliminated_plant_groups,
                                                 t_start,
                                                 group_died=True)
            plant_group.removePlantsAtIndices(kill_indices)
            plant_group.recruitPlants()

            # Add number of recruited plants to counter
            number_of_plants += plant_group.getNumberOfPlants()

        # Stop MANGA execution if no plants exist or were recruited
        if number_of_plants == 0:
            print("INFO: MANGA execution stopped because all plants died and "
                  "no new plant were recruited.")
            exit()
        self.visualization_concept.update(plant_groups, t_end)

    def finish(self, time):
        """
        Define last action when model run is finished.
        Args:
            time (float): start time of last time step
        """
        self.visualization_concept.show(time)
        plant_groups = self.population_concept.getPlantGroups()
        # Write output in last time step, even if not defined in the project
        # file
        self.model_output_concept.writeOutput(plant_groups, time, force_output=True)

    def setResources(self, ag_resources, bg_resources):
        """
        Set below- and above-ground resource arrays.
        Args:
            ag_resources (array): above-ground resource factors, shape(number_of_plants)
            bg_resources (array): below-ground resource factors, shape(number_of_plants)
        """
        self.aboveground_resources = ag_resources
        self.belowground_resources = bg_resources

    def getResources(self):
        """
        Get below- and above-ground resource arrays.
        Returns:
            2 arrays of shape(number_of_plants)
        """
        return [self.aboveground_resources, self.belowground_resources]
