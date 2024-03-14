#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import getopt
import sys
from os import path
from ProjectLib import XMLtoProject
from TimeLoopLib import DynamicTimeStep
import datetime


class Model:
    """
    pyMANGA model.
    Class to run pyMANGA externally.
    """
    def __init__(self, project_file):
        """
        Args:
            project_file (str): path to project-file
        """
        self.prj = XMLtoProject(xml_project_file=project_file)

    def createExternalTimeStepper(self, t_0=0):
        """
        Initialize time stepper for external use.
        Args:
            t_0 (float): start time, default: 0
        """
        from TimeLoopLib import ExternalDynamicTimeStep
        self.timestepper = ExternalDynamicTimeStep(self.prj, t_0)

    def setSteps(self, step_ag, step_bg):
        """
        Set steps for above- and below-ground updates.
        Args:
            step_ag (int): n-th time step to update above-ground resources (i.e., =1, update every time step)
            step_bg (int): n-th time step to update below-ground resources (i.e., =1, update every time step)
        """
        self.timestepper.setSteps(step_ag, step_bg)

    def setResources(self, ag_resources, bg_resources):
        """
        Transfer resources to time stepper.
        Args:
            ag_resources (array): above-ground resource factor (shape: no_trees)
            bg_resources (array): below-ground resource factor (shape: no_trees)
        """
        self.timestepper.setResources(ag_resources, bg_resources)

    def getResources(self):
        """
        Get resources of the current time step.
        Returns:

        """
        return self.timestepper.getResources()

    def propagateModel(self, t_end):
        """
        Propagate the model from the last time step to the next, i.e., run one time step.
        Args:
            t_end (float): end of the next timestep
        """
        self.timestepper.step(t_end)

    def setBelowgroundInformation(self, **args):
        """
        Set information required in selected below-ground module.
        """
        self.prj.getBelowgroundResourceConcept().setExternalInformation(**args)

    def getBelowgroundInformation(self):
        """
        Return information from selected below-ground module.
        """
        return self.prj.getBelowgroundResourceConcept().getExternalInformation()


def main(argv):
    """
    Main module to run pyMANGA model.
    Args:
        argv (array): command line input
    """
    try:
        opts, args = getopt.getopt(argv, "hi:l", ["project_file=", "logging"])
    except getopt.GetoptError:
        print("""pyMANGA wrong usage. Type "python main.py -h"
  for additional help.""")
        sys.exit(0)
    log_flag = False
    for opt, arg in opts:
        if opt == '-h':
            print("""pyMANGA arguments:
  -i,--project_file <path/to/xml/project/file>,\n  -l, enables logging of console output to logfile.log""")
            sys.exit()
        elif opt in ("-i", "--project_file"):
            project_file = str(arg)
        elif opt in ("-l", "--logging"):
            log_flag = True
    
    if log_flag:
        # Duplicate output stream (logfile) back to stdout for console output
        class DualOutput:
            def __init__(self, *outputs):
                self.outputs = outputs

            def write(self, text):
                for output in self.outputs:
                    output.write(text)

            def flush(self):
                for output in self.outputs:
                    output.flush()
        file_output = open('logfile.log', 'wt')
        dual_output = DualOutput(file_output, sys.stdout)
        sys.stdout = dual_output

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
