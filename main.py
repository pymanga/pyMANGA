#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getopt
import sys
from ProjectLib import XMLtoProject
from TimeLoopLib import TreeDynamicTimeStepping


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:",
                                   ["project_file="])
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
    main(sys.argv[1:])
