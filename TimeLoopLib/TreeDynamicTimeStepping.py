#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""


class TreeDynamicTimeStepping:
    def __init__(self, project):
        self.aboveground_competition = project.getAbovegroundCompetition()
        self.belowground_competition = project.getBelowgroundCompetition()
        self.death_and_growth_concept = project.getDeathAndGrowthConcept()
        self.population = project.getPopulation()
        self.visualization = project.getVisualization()
        self.visualization.update(self.population.getTreeGroups(), "Begin")

    def step(self, t_start, t_end):
        self.aboveground_competition.prepareNextTimeStep(t_start, t_end)
        self.belowground_competition.prepareNextTimeStep(t_start, t_end)
        self.death_and_growth_concept.prepareNextTimeStep(t_start, t_end)
        tree_groups = self.population.getTreeGroups()
        for group_name, tree_group in tree_groups.items():
            for tree in tree_group.getTrees():
                x, y = tree.getPosition()
                geometry = tree.getGeometry()
                parameter = tree.getParameter()
                self.aboveground_competition.addTree(x, y, geometry, parameter)
                self.belowground_competition.addTree(x, y, geometry, parameter)

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
        self.visualization.update(tree_groups, t_end)

    def finish(self, time):
        self.visualization.show(time)