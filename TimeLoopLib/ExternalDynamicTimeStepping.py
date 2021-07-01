#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""


class ExternalDynamicTimeStepping:
    def __init__(self, project, t_0):
        self.aboveground_competition = project.getAbovegroundCompetition()
        self.belowground_competition = project.getBelowgroundCompetition()
        self.death_and_growth_concept = project.getDeathAndGrowthConcept()
        self.population = project.getPopulation()
        ## Output configuration
        self.tree_output = project.getTreeOutput()
        ## Usability for OGS & check if BG concept works with OGS
        self.t_step_begin = t_0

        #TODO: We need a nice check for ogs usability?!
        try:
            self.belowground_competition.getOGSAccessible()
        except AttributeError:
            raise AttributeError(
                """In order to use MANGA as OGS python boundary condition,
                    one has to use a corresponding belowground competition
                    concept. Please see documentation for further details!""")

    def step(self, t_end):
        t_start = self.t_step_begin
        self.aboveground_competition.prepareNextTimeStep(t_start, t_end)
        self.belowground_competition.prepareNextTimeStep(t_start, t_end)
        self.death_and_growth_concept.prepareNextTimeStep(t_start, t_end)
        tree_groups = self.population.getTreeGroups()
        self.tree_output.writeOutput(tree_groups, t_start)
        for group_name, tree_group in tree_groups.items():
            for tree in tree_group.getTrees():

                self.aboveground_competition.addTree(tree)
                self.belowground_competition.addTree(tree)

        self.aboveground_competition.calculateAbovegroundResources()
        self.belowground_competition.calculateBelowgroundResources()
        belowground_resources = (
            self.belowground_competition.getBelowgroundResources())
        aboveground_resources = (
            self.aboveground_competition.getAbovegroundResources())
        j = 0
        for group_name, tree_group in tree_groups.items():
            kill_indices = []
            for tree, i in zip(tree_group.getTrees(),
                               range(tree_group.getNumberOfTrees())):
                self.death_and_growth_concept.progressTree(
                    tree, aboveground_resources[j], belowground_resources[j])
                if not tree.getSurvival():
                    kill_indices.append(i)
                j += 1
            tree_group.removeTreesAtIndices(kill_indices)
            tree_group.recruitTrees()
        t_end = self.t_step_begin
