import sys
from os import path
import os
import logging

manga_root_directory = path.dirname(
    path.dirname(path.abspath(__file__)))
sys.path.append(manga_root_directory)

from ProjectLib import XMLtoProject
from TimeLoopLib import TreeDynamicTimeStepping
import unittest
import glob
from lxml import etree
import pandas as pd


## Derived from unittest.Testcase
#  This class will manage the CI tests for the git repository
class AutomatedBenchmarkTests(unittest.TestCase):
    @classmethod
    ## Here, all setups listed in "Benchmarks/BenchmarkList.xml" are added to
    #  the tests. For each of the listed setup, a runtime test and one
    #  comparison with reference files is performed. Please make sure to save
    #  reference files in "PathToBenchmarkProject/ReferenceFiles/ProjectName".
    def setUpClass(cls):
        tree = etree.parse(path.join(manga_root_directory,
                                     "Benchmarks/BenchmarkList.xml"))
        root = tree.getroot()
        cls.manga_root_directory = manga_root_directory
        cls.setup_list = []
        cls.iterate(cls, root,
                     path.join(manga_root_directory,
                               "Benchmarks"),
                     cls.setup_list)

    ## Helper to identify listed Benchmarks
    def iterate(self, parent, existing_path, setup_list):
        for tag in parent:
            tag.text = tag.text.strip()
            if (tag.text) == "":
                new_path = path.join(existing_path, tag.tag)
                self.iterate(self, tag, new_path, setup_list)
            else:
                setup_file = (path.join(existing_path, tag.text))
                setup_list.append(setup_file)

    ## For each of the listed benchmarks, the tests are run as a subtest.
    #  Each subtest consists of "cleanup", "model_run", "comparison", "cleanup"
    def test_benchmarks(self):
        for i in range(len(self.setup_list)):
            setup = self.setup_list[i]
            with self.subTest(i=setup):
                logging.info("Testing project" + setup)
                self.clean_output_dir(setup)
                self.model_run(setup)
                self.compare_to_reference(setup)
                self.clean_output_dir(setup)
                logging.info("Success!")

    ## Runtime check
    def model_run(self, project):
        # Test of MANGA project file and run the model
        prj = XMLtoProject(xml_project_file=project)
        time_stepper = TreeDynamicTimeStepping(prj)
        prj.runProject(time_stepper)

    ## Comparison of benchmark results to reference files
    def compare_to_reference(self, project):
        e, filename = os.path.split(project)
        comparison_file_dir = path.join(path.dirname(project),
                                        "ReferenceFiles",
                                        filename.strip(".xml"))
        files_comparison = os.listdir(comparison_file_dir)
        # Query whether a reference file for the setup is not available
        output_dir = self.find_output_dir(project)
        if output_dir is not None:
            self.assertFalse(len(files_comparison) == 0,
                             "No reference files found.")
            files_result = glob.glob(path.join(output_dir, "*"))
            if files_result:
                for y in range(len(files_result)):
                    df1 = pd.read_csv(files_result[y],
                                delimiter='\t').round(5)
                    df2 = pd.read_csv(
                        path.join(comparison_file_dir,
                                  files_comparison[y]),
                        delimiter='\t').round(5)
                    test = (df1.compare(df2).values.any()) == 0

                    self.assertTrue(
                        test, str(df1.compare(df2)) +
                        "Simulation and reference differ for " +
                        files_result[y])

    ## Helpfer to find output directory for cleanup functions
    def find_output_dir(self, project):
        tree = etree.parse(project)
        root = tree.getroot()
        output = root.find("tree_output")
        output_type = output.find("type").text.strip()
        if not output_type == "NONE":
            output_dir = path.join(self.manga_root_directory,
                                   output.find("output_dir").text.strip())
            return output_dir
        else:
            return None

    # Cleanup of benchmark output directory
    def clean_output_dir(self, project):
        output_dir = self.find_output_dir(project)
        if output_dir is not None:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            else:
                old_results = glob.glob(path.join(output_dir, "*.csv"))
                if old_results:
                    for result in old_results:
                        os.remove(result)

if __name__ == "__main__":
    unittest.main()
