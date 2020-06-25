from ProjectLib import XMLtoProject
from TimeLoopLib import TreeDynamicTimeStepping
import unittest
import glob
import os

filepathExampleSetups = "./ProjectLib/ExampleSetups/*.xml"
xml = glob.glob(filepathExampleSetups)
e = []
for xmlfile in xml:
    resultsFilepath = "./ProjectLib/ExampleSetups/testoutputs/*.*"
    results = glob.glob(resultsFilepath)
    for result in results:
        os.remove(result)
    print("________________________________________________")
    print("In the following the setup", xmlfile, "is tested.")

    class MyTest(unittest.TestCase):
        filepathExampleSetups = "./ProjectLib/ExampleSetups/*.xml"

        def test(self):
            try:
                prj = XMLtoProject(xml_project_file=xmlfile)
                time_stepper = TreeDynamicTimeStepping(prj)
                prj.runProject(time_stepper)
            except:
                self.fail(e.append(xmlfile))

    if __name__ == "__main__":
        unittest.main(exit=False)
    print("The setup", xmlfile, "was tested.")
    print("________________________________________________")
print("The testing of all example setups is finished.")
print("")
resultfile = open("results", "w")
resultfile.write("Result of the test\n")
resultfile.write("\n")
if e:
    if len(e) == 1:
        print("An error occured while testing the following example setup:")
        resultfile.write(
            "Unfortunately an error occured while testing the following example setup:\n"
        )
        resultfile.write("\n")
    else:
        print("Errors occured while testing the following example setups:")
        resultfile.write(
            "Unfortunately errors occured while testing the following example setups:\n"
        )
        resultfile.write("\n")
    n = range(len(e))
    for x in n:
        print("")
        print(e[x])
        resultfile.write(e[x])
        resultfile.write("\n")
        resultfile.write("\n")
    print("")
else:
    resultfile.write("The tests of all example setups were sucessful.")
    print("The tests of all example setups were successful.")
    print("")
