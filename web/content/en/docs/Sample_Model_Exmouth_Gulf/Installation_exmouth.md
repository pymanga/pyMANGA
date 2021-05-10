---
title: "Do it yourself"
linkTitle: "Do it yourself"
weight: 4
description:
---

The model setup of the "Full Model" is located in the following folder in the current version of pyMANGA:

	./Benchmarks/Exmouth_Gulf/full_model

In order to start a model run with the setup on your own computer, file path references to input files have to be adjusted in the XML control file.
All file paths in the control file are absolute, so each path starts with "/home/..." under Ubuntu and with the letter of the drive under Windows.
If the location of the setup is not changed, the control file is located under the following path:

	./Benchmarks/Exmouth_Gulf/full_model/setup_pymanga.xml

In the control file ("setup_pymanga.xml") you have to specify the file path of the folder with the OGS input files (line 18), the file with the parameterization of the tree growth model (line 36) and the folder for the output of the model results (line 62).
You can also choose an individual file location as output location; it is only important that this folder also exists and is empty - pyMANGA does not automatically create non-existing output locations and does not delete existing files in this.

So an example of the file paths in the order mentioned above might look like the following:

	/home/Dokumente/pyMANGA-master/Benchmarks/Exmouth_Gulf/full_model/TreeOutput

	/home/Dokumente/pyMANGA-master/Benchmarks/Exmouth_Gulf/full_model/Avicennia.py

	/home/Dokumente/pyMANGA-master/Benchmarks/Exmouth_Gulf/full_model


Groundwater modeling with OGS is performed using an additional Python script.
Among other things, this script provides values for the tidal range from the file "EXM_Jan-Jul_2019.txt" for OGS, puts these data into a loop (since the modeling period is significantly longer than the period of the tidal data) and provides an adjustment of the mean water level.
The file location of the "EXM_Jan-Jul_2019.txt"-file must be adapted to the local folder structure, in the script ("python_script.py") at line 140 f.

The setup can now be started by opening a terminal in the main level of pyMANGA by entering the command

	python3 main.py -i /Benchmarks/Exmouth_Gulf/full_model/setup_pymanga.xml

The general form would be as follows:

	python3 absolute/path/to/main.py -i absolute/path/to/full_model/setup_pymanga.xml

If you have any questions or problems, please feel free to contact us.
