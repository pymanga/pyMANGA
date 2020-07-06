import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from ProjectLib import XMLtoProject
from TimeLoopLib import TreeDynamicTimeStepping
import unittest
import glob
import os

filepath_example_setups = path.join(path.dirname(path.abspath(__file__)),"Test_Setups_large/*.xml")
xml = glob.glob(filepath_example_setups)
errors = []
if xml:
    for xml_file in xml:
        filepath_results = path.join(path.dirname(path.abspath(__file__)),"Test_Setups_large/testoutputs/*.*")
        results = glob.glob(filepath_results)
        for result in results:
            os.remove(result)
        print("________________________________________________")
        print("In the following the setup", xml_file, "is tested.")
    
        class MyTest(unittest.TestCase):
    
            def test(self):
                try:
                    prj = XMLtoProject(xml_project_file=xml_file)
                    time_stepper = TreeDynamicTimeStepping(prj)
                    prj.runProject(time_stepper)
                except:
                    self.fail(errors.append(xml_file))
    
        if __name__ == "__main__":
            unittest.main(exit=False)
        print("The setup", xml_file, "was tested.")
        print("________________________________________________")
    print("The testing of all example setups is finished.")
    print("")
    if errors:
        if len(errors) == 1:
            print("An error occured while testing the following example setup:")
        else:
            print("Errors occured while testing the following example setups:")
        n = range(len(errors))
        for x in n:
            print("")
            print(errors[x])
        print("")
    else:
        print("The tests of all example setups were successful.")
        print("")
else: print("unfortunately no project-file could be found.")
