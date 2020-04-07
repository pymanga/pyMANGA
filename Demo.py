from ProjectLib import XMLtoProject
from TimeLoopLib import TreeDynamicTimeStepping
import unittest

class TestNeueKlasse(unittest.TestCase):	
    	def test_code_run_files_without_errors(self):
        	try:
            		prj = XMLtoProject(xml_project_file="Demo.xml")
            		time_stepper = TreeDynamicTimeStepping(prj)
            		prj.runProject(time_stepper)
        	except:
            		self.fail("Fehler")
if __name__ == '__main__':
    unittest.main()
