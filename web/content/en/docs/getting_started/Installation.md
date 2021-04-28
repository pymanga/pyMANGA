---
title: "Installation of pyMANGA"
linkTitle: "Installation of pyMANGA"
weight: 1
description: 
---
<head>
<style type="text/css">
<!--
details summary {color: white; background: #00305E; margin-bottom: 1em;}
-->
</style>
</head>

The software pyMANGA represents a coupling between a tree growth and a groundwater modelling program.
The software "Bettina" is used for the modeling of plant growth and the software <a href="https://www.opengeosys.org/" target="_blank">**OpenGeoSys**</a> for the modeling of groundwater.

Since the tree growth model and the coupling between the two programs are written in **Python**, a **Python compiler** is required to run the **pyMANGA** program.
During the installation a local library with different **Python modules** is installed on your computer.
These modules contain source code that is difficult to formulate or frequently used - so it does not need to be written in the program, but can be easily retrieved from the library.
Because the installation differs between operating systems, please select your operating system below.


In order to run **MANGA**, some modules for the **Python compiler** must be installed.
Since the system requirements differ greatly between the various operating systems, the installation is described separately for each one.

<details>
<summary>Installation of Python in Ubuntu</summary>
<p>

**Ubuntu 18.04** includes a first installation of (**Python 2** and) **Python 3** by default.
In order to check which version is currently on the computer, after opening a new terminal window with the key combination **"CTRL + Alt + T "**, a version query can be started with the command:

	• python3 -V 

It is recommended to update the package directory of the operating system first.
To update the current version, you can use the commands 

	• sudo apt update
 
and 

	• sudo apt -y upgrade 

to update the whole system - and thus the **Python 3** package.
The updated version can be checked again via the command

	• python3 -V

If unexpected problems occur, you can use the command

	• sudo apt-get install python3

to (re)install the package.
</p>
</details>

<details>
<summary>Installation of Python in Windows</summary>
<p>

To run **MANGA** (Mangrove groundwater salinity feedback model), you must first obtain an **interpreter** for the **Python** programming language.
An example would be **python<sup>T</sup><sup>M</sup>**.
To do this, open your browser and go to ***Python.org***.
In the drop-down menu under ***Download*** you will find the current release version for your operating system of **Python** (this manual describes the procedure for Windows, see <a href="/docs/getting_started/installation/#Figure_1">Figure 1</a>).

<figure>
<a name="Figure_1"></a>
<img src="/pictures/Auswahl_Menue_zum_Downloaden_der_Windows_Variante_von_pythonTM.jpg">
<figcaption><font size = "1"><i><b>Figure 1: </b>Selection menu for downloading the Windows variant of python<sup>T</sup><sup>M</sup>.</i></font></figcaption>
</figure><p>

<figure>
<a name="Figure_2"></a>
<img src="/pictures/zu_waehlender_Link_für_das_Downloaden_von_python-3_7_7.jpg">
<figcaption><font size = "1"><i><b>Figure 2: </b>link to be chosen for downloading python-3.7.7</i></font></figcaption>
</figure><p>

Execute the downloaded file (***python-3.7.7-amd64.exe***) like a normal Windows exe and install it on your computer (see <a href="/docs/getting_started/installation/#Figure_3">Figure 3</a>). 

<figure>
<a name="Figure_3"></a>
<img src="/pictures/Ausfuehrung_der_Windows_exe_von_Python_3_7_7.jpg">
<figcaption><font size = "1"><i><b>Figure 3: </b>Running the Windows exe of Python 3.7.7.</i></font></figcaption>
</figure><p>

This completes the **Python** installation. 
<!-- To start **MANGA** some additional preparations have to be made. Go to the subdirectory Preparation and select the appropriate file before your operating system. -->
</p>
</details>


After you have set up **Python** on your computer, the next step is to install **pyMANGA**.
You can do this either by cloning the [git-repositories](https://github.com/jbathmann/pyMANGA/ "https://github.com/jbathmann/pyMANGA/") (for advanced users) or by following the instructions below.
</p>

<details>
<summary >Installation of pyMANGA in Ubuntu <a name="Installation_Ubuntu"></a></summary>
<p>

In order to run **pyMANGA**, you may need to install modules that are not yet in the **Python** library but are required by pyMANGA.
Since **Python** also plays an important role in the **Ubuntu** operating system, the pre-installed library is very extensive.
Therefore it is recommended to install the program first and to install any missing modules after the first execution of the program - **pyMANGA** will tell you which modules are needed.

The current version of **pyMANGA** can be found on this [homepage](https://github.com/jbathmann/pyMANGA/ "https://github.com/jbathmann/pyMANGA/").
Download the source code of the program as shown in <a href="/docs/getting_started/installation/#Figure_4">Figure 4</a> as zip file.

<figure>
<a name="Figure_4"></a>
<img src="/pictures/ubuntu_download.png">
<figcaption><font size = "1"><i><b>Figure 4: </b>Download of <b>pyMANGA</b> as zip-file

</i></font></figcaption>
</figure><p>

This zip file must now be unpacked to any location.
Make sure that there are no spaces and no umlauts (like ä,ö,ü,ß) in the file path.

The program is now executable.
Open a terminal window with the key combination **Ctrl + Alt + T** and navigate to the main level of the program.
Alternatively, you can also choose the graphical way by navigating to the location via Files.
There you can open the console by right-clicking and in the menu that opens, you have to use the field "Open in Terminal" to open a terminal window, where you are already in the main level of the program.

<figure>
<a name="Figure_5"></a>
<img src="/pictures/ubuntu_Hauptebene_pyMANGA.png">
<figcaption><font size = "1"><i><b>Figure 5: </b> Main level of pyMANGA</i></font></figcaption>
</figure><p>

By typing 

	• python3 main.py

the program will now be started.
If **pyMANGA** cannot yet be executed due to missing modules in the local Python library - as mentioned at the beginning - one of the missing packages is displayed in an error message.
For the installation of **Python modules**, **pip** ("Pip installs Python") is suitable.
By opening a terminal window (key combination **Ctrl + Alt + T**) and entering the command

	• sudo apt-get install python3-pip

pip can be installed.

To add a **Python module** to the library with **pip** the following command must be entered into a terminal:

	• pip3 install name_of_the_module

If no manual changes have been made to the standard Python library, the modules "numpy", "vtk", "lxml" and "matplotlib" are missing to run **pyMANGA**.
These must all be installed, so the first command would look like this for the module "numpy":

	• pip3 install numpy

The only exception is the module "vtk".
In order to be able to perform calculations with pyMANGA at a later time, which also take the **groundwater flow** into account, **a certain version** is required for this module.
If you do not want to install the latest version of a module with pip, the command looks like this:

	• pip3 install vtk==8.1.2

After the missing module is installed, restart **pyMANGA**.
If any other **Python modules** are missing now, **pyMANGA** will again output one of them as missing prerequisite.
Repeat this step until all **Python modules** are installed.
If this is the case, you should get the following output:


	Traceback (most recent call last):
	  File "main.py", line 26, in main
	    prj = XMLtoProject(xml_project_file=project_file)
	UnboundLocalError: local variable 'project_file' referenced before assignment
	
	During handling of the above exception, another exception occurred:
	
	Traceback (most recent call last):
	  File "main.py", line 38, in <module>
	    main(sys.argv[1:])
	  File "main.py", line 28, in main
	    raise UnboundLocalError('Wrong usage of pyMANGA. Type "python' +
	UnboundLocalError: Wrong usage of pyMANGA. Type "python main.py -h" for additional help.


Even if you get this error message first, it means that **pyMANGA** is installed and is runable correctly.
The calculation of a first example setup is explained in the section  <a href="/docs/getting_started/first_applications_of_pymanga/">First Applications of **pyMANGA**</a> of this short tutorial.
</p>
</details>


<details>
<summary>Installation of pyMANGA in Windows</summary>
<p>

To be able to run **MANGA**, some modules for the **Python Compiler** must be installed.
You have to open the **prompt** for this.
You can easily find it by searching for it by typing **"Command Prompt"** and opening it with a **mouse click**.
Since MANGA is a line program, everything happens at the command prompt (see <a href="/docs/getting_started/installation/#Figure_6">Figure 6</a>).

<figure>
<a name="Figure_6"></a>
<img src="/pictures/oeffnen_der_Eingabeaufforderung.jpg">
<figcaption><font size = "1"><i><b>Figure 6 :</b>open the command prompt.</i></font></figcaption>
</figure><p>

Now the following modules ***numpy***, ***vtk***, ***lxml*** and ***matplotlib*** must be installed.
We start with the **module** ***numpy***.
Type the code shown in the **prompt** to install the **module** (see <a href="/docs/getting_started/installation/#Figure_7">Figure 7</a>).

	• py -3.7 -m pip install numpy						     		[1]

<figure>
<a name="Figure_7"></a>
<img src="/pictures/Beispielhafte_Installation_des_Moduls_numpy.jpg">
<figcaption><font size = "1"><i><b>Figure 7: </b> Exemplary installation of the numpy module.</i></font></figcaption>
</figure><p>

Do the same for the other three **modules** with the following code

	• py -3.7 -m pip install vtk						     		[2]
	• py -3.7 -m pip install lxml					  	     		[3]
	• py -3.7 -m pip install matplotlib					     		[4]

Note: If the prompt says that ***pip*** is not up to date, you can use **upgrade** ***pip*** to update it.
However, this is not mandatory.

Some explenations: ***py*** means you are calling **Python**. 
Where **-3.7** is the version you are using.
***-m*** means you are calling a module, in this case ***pip***, which is used to install other **modules**.
Finally, the **module** **name** of the **module** to be installed follows.
Now the preparations for using the **compiler** are finished.
As a next step you have to download the program **MANGA***, if you haven't done so already.
To do this, go to the following website [**Link**](https://github.com/jbathmann/pyMANGA/ "https://github.com/jbathmann/pyMANGA/") and download the program as a zip file and save it on your computer (see <a href="/docs/getting_started/installation/#Figure_8">Figure 8</a>).

<figure>
<a name="Figure_8"></a>
<img src="/pictures/Download_von_pyMANGA.jpg">
<figcaption><font size = "1"><i><b>Figure 8: </b> Download from pyMANGA.</i></font></figcaption>
</figure><p>

Then unzip the file (***pyMANGA-master.zip***) to your desktop.
It contains all the program components of **MANGA**, including ***main.py***, which is the execution file that must be called to execute the program.
To do so, open the **folder** and **right-click** in an empty area of the **folder** to open the command **prompt** (see <a href="/docs/getting_started/installation/#Figure_9">Figure 9</a>) and enter the following code.

	• py main.py -h								     		[5]

Again, ***py*** means Python is called, ***main.py*** represents the file to be called, and ***-h*** calls the help.

<figure>
<a name="Figure_9"></a>
<img src="/pictures/oeffnen_der_Eingabeaufforderung_im_pyMANGA_Ordner.jpg">
<figcaption><font size = "1"><i><b>Figure 9: </b> open the command prompt in the pyMANGA folder.</i></font></figcaption>
</figure><p>

Note: The command **prompt** is called in the **folder** so that the **folder path** does not have to be entered each time.
On Windows 10, this is only possible by downloading ***cmd add to context menu.zip*** from the following [web page](https://www.giga.de/downloads/windows-10/tipps/windows-10-wieder-die-eingabeaufforderung-im-kontextmenue-anzeigen/ "https://www.giga.de/downloads/windows-10/tipps/windows-10-wieder-die- prompt in-context menu-display/") and running it as described on the page.
Alternatively, you can use Command **Prompt**, which you can find in Windows **Search** with the search term **"Command Prompt"**, and specify the complete file path, which in this example is ***C:\Users\...\Desktop\pyMANGA-master***.
To find your file path, **right-click** on the ***pyMANGA-master*** **folder** and go to **Properties**.
Here you will find the information about the location of the folder to which you have to add a \ to the **name** of the **folder**

</p>
</details>
      
