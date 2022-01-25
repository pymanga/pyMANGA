#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de, marie-christin.wimmler@tu-dresden.de
"""


class TreeDynamicTimeStepping:
    def __init__(self, project):
        self.aboveground_competition = project.getAbovegroundCompetition()
        self.belowground_competition = project.getBelowgroundCompetition()
        self.death_and_growth_concept = project.getDeathAndGrowthConcept()
        self.population = project.getPopulation()
        self.visualization = project.getVisualization()
        self.visualization.update(self.population.getTreeGroups(), "Begin")
        ## Output configuration
        self.tree_output = project.getTreeOutput()

        self.aboveground_resources = []
        self.belowground_resources = []

    ## This progresses one time step, by updating tree population and above-
    # and below-ground resources. Not all concepts have to be called with
    # the same frequency (i.e. only if update_x is true).
    def step(self, t_start, t_end, update_ag, update_bg):
        if update_ag:
            self.aboveground_competition.prepareNextTimeStep(t_start, t_end)
        if update_bg:
            self.belowground_competition.prepareNextTimeStep(t_start, t_end)
        self.death_and_growth_concept.prepareNextTimeStep(t_start, t_end)
        tree_groups = self.population.getTreeGroups()

        self.tree_output.writeOutput(tree_groups, t_start)
        for group_name, tree_group in tree_groups.items():
            for tree in tree_group.getTrees():
                if update_ag:
                    self.aboveground_competition.addTree(tree)
                if update_bg:
                    self.belowground_competition.addTree(tree)

        if update_ag:
            self.aboveground_competition.calculateAbovegroundResources()
            self.aboveground_resources = (
                self.aboveground_competition.getAbovegroundResources())
        if update_bg:
            self.belowground_competition.calculateBelowgroundResources()
            self.belowground_resources = (
                self.belowground_competition.getBelowgroundResources())
        j = 0
        for group_name, tree_group in tree_groups.items():
            kill_indices = []
            for tree, i in zip(tree_group.getTrees(),
                               range(tree_group.getNumberOfTrees())):
                ## If a new tree is recruited in the current time step and
                # the respective resource was not updated, set survival of
                # the new tree to 1
                try:
                    ag = self.aboveground_resources[j]
                    bg = self.belowground_resources[j]
                    self.death_and_growth_concept.progressTree(
                        tree, ag, bg)
                except IndexError:
                    tree.setSurvival(1)

                if not tree.getSurvival():
                    kill_indices.append(i)

                j += 1
            tree_group.removeTreesAtIndices(kill_indices)
            tree_group.recruitTrees()
        self.visualization.update(tree_groups, t_end)

    ## Last action, when timeloop is done
    def finish(self, time):
        self.visualization.show(time)
        tree_groups = self.population.getTreeGroups()

        self.tree_output.writeOutput(tree_groups, time)

    def setResources(self, ag_resources, bg_resources):
        self.aboveground_resources = ag_resources
        self.belowground_resources = bg_resources

    def getResources(self):
        return [self.aboveground_resources, self.belowground_resources]
