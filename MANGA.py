#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getopt
import sys
from os import path
from ProjectLib import XMLtoProject
from TimeLoopLib import TreeDynamicTimeStepping


class Model():
    ## Class to run the model from other programs
    #  @param project_file: path to pymanga project file.
    #  @date: 2021 - Today
    #  @author: jasper.bathmann@ufz.de
    def __init__(self, project_file):
        self.prj = XMLtoProject(xml_project_file=project_file)
        self.t_step_begin = 0

    def createExternalTimeStepper(self, t_0=0):
        from TimeLoopLib import ExternalDynamicTimeStepping
        self.timestepper = ExternalDynamicTimeStepping(self.prj, t_0)

    ## This call propagates the model from the last timestep.
    #  Default starting point is t=0 and will be updated with every call
    #  @param t: time, for end of next timestep
    def propagateModel(self, t):
        self.timestepper.step()
        self.t_step_begin = t


def main(argv):
    #sys.path.append(path.abspath(path.dirname(__file__)))

    try:
        opts, args = getopt.getopt(argv, "hi:", ["project_file="])
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
    try:
        prj = XMLtoProject(xml_project_file=project_file)
    except UnboundLocalError:
        raise UnboundLocalError('Wrong usage of pyMANGA. Type "python' +
                                ' main.py -h" for additional help.')
    print('Running pyMANGA project ', project_file)
    time_stepper = TreeDynamicTimeStepping(prj)
    prj.runProject(time_stepper)
    print('pyMANGA project ', project_file, ' successfully evaluated.')


if __name__ == "__main__":
    sys.path.append((path.dirname(path.abspath(__file__))))
    main(sys.argv[1:])
