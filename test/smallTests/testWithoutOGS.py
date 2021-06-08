# This script tests pyMANGA using seven setups
# The first test only checks whether the setups can be calculated without
# errors
# The second test compares the calculated results with reference results

import sys
from os import path

sys.path.append(
    path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

from ProjectLib import XMLtoProject
from TimeLoopLib import TreeDynamicTimeStepping
import unittest
import glob
import os
from lxml import etree
import shutil
from pathlib import Path

manga_root_directory = path.dirname(
    path.dirname(path.dirname(path.abspath(__file__))))
filepath_examplesetups = path.join(path.dirname(path.abspath(__file__)),
                                   "testSetupsWithoutOGS/*.xml")
xml = glob.glob(filepath_examplesetups)
example_setups = []
errors = []
errors_compare = []
errors_empty_comparison = []
errors_empty_results = []

global output_exist
output_exist = str
global seperator

seperator = "/"

if xml:
    for xmlfile in xml:
        print("________________________________________________")
        print("In the following the setup", xmlfile, "is tested.")
        print("________________________________________________")

        def findChild(parent, key):
            child = parent.find(key)
            return child

        global output_dir
        global output_type

        tree = etree.parse(xmlfile)
        root = tree.getroot()
        for tag in root.iter():
            tag.text = tag.text.strip()

        output = findChild(root, "tree_output")
        output_type_xml_element = findChild(output, "type")
        output_type = output_type_xml_element.text

        if not output_type == "NONE":
            output_dir_xml_element = findChild(output, "output_dir")
            output_dir = path.join(manga_root_directory,
                                   output_dir_xml_element.text)

            if not os.path.exists(output_dir):
                output_exist = False
                os.makedirs(output_dir)
            else:
                output_exist = True
                old_results = glob.glob(path.join(output_dir, "*.*"))
                if old_results:
                    for result in old_results:
                        os.remove(result)
                        e, filename = os.path.split(xmlfile)
        else:
            errors_empty_results.append(xmlfile)

        e, filename = os.path.split(xmlfile)
        comparison_file_dir_in_pieces = (path.join(path.dirname(
            path.abspath(__file__))), "referenceFiles", filename, "*.*")
        comparison_file_dir = seperator.join(comparison_file_dir_in_pieces)
        files_comparison = glob.glob(comparison_file_dir)
        example_setups.append(filename)

        class MyTest(unittest.TestCase):
            def test1(self):
                # Test of MANGA project file and the correct calculation of its
                try:
                    prj = XMLtoProject(xml_project_file=xmlfile)
                    time_stepper = TreeDynamicTimeStepping(prj)
                    prj.runProject(time_stepper)
                # Storing failed test for clear evaluation
                except:
                    self.fail(errors.append(xmlfile))

            def test2(self):
                # Query whether a reference file for the setup is not available
                if not files_comparison:
                    errors_empty_comparison.append(xmlfile)
#               If a reference file is available, it will be compared with the
#               calculated results
                else:
                    files_result = glob.glob(path.join(output_dir, "*.*"))
                    for file_comparison, file_result in zip(
                            (files_comparison), (files_result)):
                        try:
                            assert (Path(file_comparison).read_bytes() ==
                                    Path(file_result).read_bytes()), \
                                f"{file_comparison!r} != {file_result!r}"
                        except:
                            self.fail(errors_compare.append(xmlfile))

        if __name__ == "__main__":
            unittest.main(exit=False)

        # remove created output
        if not output_type == "NONE":
            if not output_exist:
                shutil.rmtree((output_dir[:-1]), ignore_errors=True)
            elif output_exist:
                old_results = glob.glob(path.join(output_dir, "*.*"))
                for result in old_results:
                    os.remove(result)

        print("The setup", xmlfile, "was tested.")
        print("________________________________________________")

    print("")
    print("The testing of all example setups is finished.")
    print("")
    print("________________________________________________")
    print("________________________________________________")
    print("")
    print("Report")
    print("________________________________________________")
    print("________________________________________________")
    print("")
    if not len(example_setups) == 1:
        print("The following sample setups have been tested:")
    else:
        print("The following sample setup have been tested:")
    print("")
    for setup in example_setups:
        print("")
        print(setup)

    print("________________________________________________")
    print("________________________________________________")
    print("")
    print("Result of the first test:")
    print("")

    if errors:
        if len(errors) == 1:
            print(
                "An error occured while testing the following example setup:")
        else:
            print("Errors occured while testing the following example setups:")
        n = range(len(errors))
        for x in n:
            print("")
            print(errors[x])
        print("")
    else:
        print("The tests of all example setups were successful.")

    print("________________________________________________")
    print("________________________________________________")
    print("")
    print("Result of the second test:")
    print("")

    if errors_empty_comparison:
        if len(errors_empty_comparison) == 1:
            print("There are no files with which the result of the setup",
                  errors_empty_comparison, "could be compared.")
        else:
            print("There are missing files for the comparison of the result ",
                  "of the following example-setups:")
            print("")
            n = range(len(errors_empty_comparison))
            for x in n:
                print("")
                print(errors_empty_comparison[x])
                print("")
    else:
        if errors_compare:
            if len(errors_compare) == 1:
                print("An error occurred when comparing the result of the "
                      "following example setup with the comparison files:")
                print("")
            else:
                print("An error occurred when comparing the result of the "
                      "following example setups with the comparison files:")
                print("")
            n = range(len(errors_compare))
            for x in n:
                print("")
                print(errors_compare[x])
                print("")
            if errors_empty_results:
                if len(errors_empty_results) == 1:
                    print("Please also note that the following sample setup "
                          "does not save model results and therefore could "
                          "not be checked:")
                else:
                    print("Please also note that the following sample setups "
                          "do not save model results and therefore could not "
                          "be checked:")
                    print("")
                n = len(errors_empty_results)
                for x in n:
                    print(errors_empty_results[x])
                    print("")
        else:
            if errors_empty_results:
                if len(errors_empty_results) == 1:
                    print("The comparison of the result of the example setup "
                          "with the comparison files was successful. Please "
                          "note, however, that the following sample setup do "
                          "not save model results and therefore could not be "
                          "checked:")
                else:
                    print("The comparison of the result of the example setups "
                          "with the comparison files was successful. Please "
                          "note, however, that the following sample setups do "
                          "not save model results and therefore could not be "
                          "checked:")
                    print("")
                n = len(errors_empty_results)
                for x in n:
                    print("")
                    print(errors_compare[x])
                    print("")
                else:
                    print("The comparison of the result of the example setups "
                          "with the comparison files was successful.")
            else:
                print("The comparison of the result of the example setups "
                      "with the comparison files was successful.")
    print("________________________________________________")
    print("________________________________________________")
else:
    print("Unfortunately no project-file could be found.")
