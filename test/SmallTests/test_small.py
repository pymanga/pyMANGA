import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from ProjectLib import XMLtoProject
from TimeLoopLib import TreeDynamicTimeStepping
import unittest
import glob
import os
from lxml import etree
import shutil
from utils import get_project_root

manga_root_directory = str(get_project_root())
filepath_examplesetups = path.join(path.dirname(path.abspath(__file__)),"Test_Setups_small/*.xml")
xml = glob.glob(filepath_examplesetups)
errors = []
global output_exist
output_exist = str
if xml:
    for xmlfile in xml:
        print("________________________________________________")
        print("In the following the setup", xmlfile, "is tested.")
        print("________________________________________________")


        def findChild( parent, key):
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
            #output_dir =  path.join(path.dirname(path.abspath(__file__)), output_dir_xml_element.text)
            output_dir = path.join(manga_root_directory, output_dir_xml_element.text)
            
            if not os.path.exists(output_dir):
                output_exist = False                   
                os.makedirs(output_dir)
            else:
                output_exist = True
                old_results = glob.glob(path.join(output_dir,"*.*"))
                if old_results:
                    for result in old_results:
                        os.remove(result)
        else:
                output_exist = "e"
                
        class MyTest(unittest.TestCase):
            def test(self):
                try:
                    prj = XMLtoProject(xml_project_file=xmlfile)
                    time_stepper = TreeDynamicTimeStepping(prj)
                    prj.runProject(time_stepper)
                except:
                    self.fail(errors.append(xmlfile))
        
        if __name__ == "__main__":
            unittest.main(exit=False)
        if not output_type == "NONE":
            if not output_exist:
                shutil.rmtree((output_dir[:-1]), ignore_errors=True)
            elif output_exist:
                old_results = glob.glob(path.join(output_dir,"*.*"))
                for result in old_results:
                    os.remove(result)
        
    print("The setup", xmlfile, "was tested.")
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
else: print("Unfortunately no project-file could be found.")