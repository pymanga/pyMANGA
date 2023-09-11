#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de, marie-christin.wimmler@tu-dresden.de
"""

import getopt
import sys
from os import path
from ProjectLib import XMLtoProject
from TimeLoopLib import DynamicTimeStep
import datetime


class Model():
    ## Class to run the model from other programs
    #  @param project_file: path to pymanga project file.
    #  @date: 2021 - Today
    #  @author: jasper.bathmann@ufz.de
    def __init__(self, project_file):
        self.prj = XMLtoProject(xml_project_file=project_file)

    def createExternalTimeStepper(self, t_0=0):
        from TimeLoopLib import ExternalDynamicTimeStep
        self.timestepper = ExternalDynamicTimeStep(self.prj, t_0)

    def setSteps(self, step_ag, step_bg):
        self.timestepper.setSteps(step_ag, step_bg)

    def setResources(self, ag_resources, bg_resources):
        self.timestepper.setResources(ag_resources, bg_resources)

    def getResources(self):
        return self.timestepper.getResources()

    ## This call propagates the model from the last timestep.
    #  Default starting point is t=0 and will be updated with every call
    #  @param t: time, for end of next timestep
    def propagateModel(self, t_end):
        self.timestepper.step(t_end)

    def setBelowgroundInformation(self, **args):
        self.prj.getBelowgroundResourceConcept().setExternalInformation(**args)

    ## Getter for external information
    def getBelowgroundInformation(self):
        return self.prj.getBelowgroundResourceConcept().getExternalInformation()


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:l", ["project_file=", "logging"])
    except getopt.GetoptError:
        print("""pyMANGA wrong usage. Type "python main.py -h"
  for additional help.""")
        sys.exit(0)
    for opt, arg in opts:
        if opt == '-h':
            print("""pyMANGA arguments:
  -i,--project_file <path/to/xml/project/file>""")
            sys.exit()
        elif opt in ("-i", "--project_file"):
            project_file = str(arg)
    t_start = datetime.datetime.now()

    try:
        prj = XMLtoProject(xml_project_file=project_file)

    except UnboundLocalError:
        raise UnboundLocalError('Wrong usage of pyMANGA. Type "python' +
                                ' main.py -h" for additional help.')
    print("--------------------\npyMANGA started at", t_start)
    print('Running pyMANGA project file:', project_file)
    time_stepper = DynamicTimeStep(prj)
    prj.runProject(time_stepper)
    t_end = datetime.datetime.now()
    print('pyMANGA project', project_file, 'successfully evaluated.')
    print("pyMANGA finished at", t_end)
    print("Total execution took", (t_end - t_start).seconds, "seconds")


if __name__ == "__main__":
    sys.path.append((path.dirname(path.abspath(__file__))))
    main(sys.argv[1:])
