# This script tests pyMANGA using seven setups
# The first test only checks whether the setups can be calculated without
# errors
# The second test compares the calculated results with reference results

import sys
from os import path
import os

manga_root_directory = path.dirname(
    path.dirname(path.abspath(__file__)))
sys.path.append(manga_root_directory)

from ProjectLib import XMLtoProject
from TimeLoopLib import TreeDynamicTimeStepping
import unittest
import glob
import os
from lxml import etree
import shutil
from pathlib import Path
import pandas as pd


tree = etree.parse(path.join(manga_root_directory,
                             "Benchmarks/BenchmarkList.xml"))
root = tree.getroot()


def iterate(parent, existing_path, setup_list):
    for tag in parent:
        tag.text = tag.text.strip()
        if (tag.text) == "":
            new_path = path.join(existing_path, tag.tag)
            iterate(tag, new_path, setup_list)
        else:
            setup_file = (path.join(existing_path, str(tag.text)))
            setup_list.append(setup_file)


setup_list = []
iterate(root, path.join(manga_root_directory, "Benchmarks"), setup_list)
example_setups = []
errors = []
errors_compare = []
errors_empty_comparison = []
errors_empty_results = []
testlist = []
global output_exist
output_exist = str

# MARKER:
if setup_list:
    for xmlfile in setup_list:
        print("________________________________________________")
        print("In the following the setup", xmlfile, "is tested.")
        print("________________________________________________")

        def findChild(parent, key):
            child = parent.find(key)
            return child

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
        comparison_file_dir = path.join(path.dirname(xmlfile),
                                        "ReferenceFiles",
                                        filename.strip(".xml"))
        files_comparison = os.listdir(comparison_file_dir)
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
                    files_result = glob.glob(path.join(output_dir, "*"))
                    if files_result:
                        for y in range(len(files_result)):
                            try:
                                test = (
                                    pd.read_csv(files_result[y],
                                                delimiter='\t').compare(
                                        pd.read_csv(
                                            path.join(comparison_file_dir,
                                                      files_comparison[y]),
                                            delimiter='\t')).values.any()) == 0
                                self.assertTrue(test)
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

    print("""
    The testing of all setups is finished.
    print("")
    ________________________________________________
    ________________________________________________
    ########
    #Report#
    ########
    ________________________________________________
    ________________________________________________
    """)
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
        print("An error occured while testing the following setup(s):")
        n = range(len(errors))
        for x in n:
            print("")
            print(errors[x])
        print("")
    else:
        print("The first test of all setups were successful.")

    print("________________________________________________")
    print("________________________________________________")
    print("")
    print("Result of the second test:")
    print("")

    if errors_empty_comparison and errors_compare:
        print('An error occured when comparing the result of the following '
              'setup:')
        for x in range(len(errors_compare)):
            print("")
            print(errors_compare[x])
            print("")
        print('It should be noted further:')
        print('There are missing files for the comparison of the result '
              'of the following setups:')
        for x in range(len(errors_empty_comparison)):
            print("")
            print(errors_empty_comparison[x])
            print("")
    elif errors_empty_comparison:
        print("There is/are missing file(s) for the comparison of the result "
              "of the following setup(s):")
        print("")
        n = range(len(errors_empty_comparison))
        for x in n:
            print("")
            print(errors_empty_comparison[x])
            print("")
        print("The comparison of the result of the other setups "
              "with the comparison files was successful.")
    else:
        if errors_compare:
            print("An error occurred when comparing the result(s) of the "
                  "following setup(s) with the comparison file(s):")
            print("")
            for x in range(len(errors_compare)):
                print("")
                print(errors_compare[x])
                print("")
            if errors_empty_results:
                print("Please also note that the following sample setup(s) "
                      "do not save model results and therefore could not "
                      "be checked:")
                print("")
                n = len(errors_empty_results)
                for x in n:
                    print(errors_empty_results[x])
                    print("")
        else:
            if errors_empty_results:
                print("""The comparison of the result of the setups
                      with the comparison files was successful. Please
                      note, however, that the following sample setups do
                      not save model results and therefore could not be
                      "checked:""")
                print("")
                n = len(errors_empty_results)
                for x in n:
                    print("")
                    print(errors_compare[x])
                    print("")
            else:
                print("The comparison of the result of the setups "
                      "with the comparison files was successful.")
    print("________________________________________________")
    print("________________________________________________")
else:
    print("Unfortunately no project-file could be found.")
