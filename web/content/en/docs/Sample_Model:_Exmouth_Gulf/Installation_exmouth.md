---
title: "Installation of the model setup"
linkTitle: "Installation of the model setup"
weight: 4
description:
---

The model setup can be downloaded here !!!link will follow after consultation!!!. The folder can be unzipped at any place, but for example the main level of the pyMANGA installation is suitable.

In order to start a model run with the setup on your own computer, file paths references to input files have to be adjusted in the XML control file. All file paths in the control file are specified absolutely, so each path starts with "/home/..." under Ubuntu and with the letter of the drive under Windows. If you install the setup folder into the pyMANGA main level, you will find the file under the path

	./Study_Site_Exmouth_Gulf/setup_pymanga.xml.

In the control file (setup_pymanga.xml) you have to specify the file path for the output of the model results (line 76) and the folder with the OGS input files (line 18). As output location you can choose an individual file location; it is only important that this folder also exists and is empty - pyMANGA does not automatically create non-existing output locations.

So an example output location for the results (1) and the folder containing the OGS input files (2) might look like the following:

	/home/Dokumente/pyMANGA-master/Study_Site_Exmouth_Gulf/output	  (1)

	/home/Dokumente/pyMANGA-master/Study_Site_Exmouth_Gulf/Input_OGS  (2)


Groundwater modeling with OGS is performed in more detail using an additional Python script. Among other things, this script provides values for the tidal range from the file "EXM_Jan-Jul_2019.txt" for OGS, puts these data into a loop (since the modeling period is significantly longer than the period of the tidal data), and provides for an adjustment of the mean water level. In the Python script there is a reference to the file location of this file, in line 140 f. the file location of the "EXM_Jan-Jul_2019.txt" file must be adapted to the respective file system.

The setup can now be started by opening a terminal in the main level of pyMANGA by entering the command: 

	python3 main.py -i /Model_Exmouth_Gulf/setup_pymanga.xml

If the default name of the setup's folder ("Model_Exmouth_Gulf") has been changed or the setup has not been installed in the pyMANGA main level the reference to the control file's file location must be adjusted accordingly. So the general form would look like this:

	python3 absolute/path/to/main.py -i absolute/path/to/Model_Exmouth_Gulf/setup_pymanga.xml
