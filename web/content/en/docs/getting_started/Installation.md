---
title: "Installation of pyMANGA"
linkTitle: "Installation of pyMANGA"
weight: 1
description: 
---

<style type="text/css">
    details summary {color: white; background: #00305E; margin-bottom: 1em;}
    @media(min-width: 992px){
      details{width: 80%}
    }
</style>

## Requirements 

The software **pyMANGA** is written in the programming language [Python](https://www.python.org/) and uses Python libraries. 
That means, during the installation a local library with different **Python modules** will be installed on your computer.
These modules contain source code that is frequently used by many programmers.

If you are new to programming, it might be convenient to install a user interface, a so-called IDE, to work with Python. 
Those IDEs make code easier to read and support the installation and management of modules, for example.
Our team is happy to use [PyCharm](https://www.jetbrains.com/pycharm/) and [Spyder](https://www.spyder-ide.org/), respectively.
Both IDEs offer a free version.

## Install Python and Python Modules

In the following, we describe how to install the following software

- Python3
- Python Modules
  - numpy
  - vtk
  - matplotlib

Because the installation differs between operating systems, please select your operating system below.

### Ubuntu

<details>
<summary>Installation of Python in Ubuntu</summary>

**Ubuntu 18.04** includes a first installation of (**Python 2** and) **Python 3** by default.
In order to check which version is currently on the computer, after opening a new terminal window with the key combination **"CTRL + Alt + T "**, a version query can be started with the command:

	python3 -V 

It is recommended to update the package directory of the operating system first.
To update the current version, you can use the commands 

	sudo apt update
 
and 

	sudo apt -y upgrade 

to update the whole system - and thus the **Python 3** package.
The updated version can be checked again via the command

	python3 -V

If unexpected problems occur, you can use the command

	sudo apt-get install python3

to (re)install the package.

</details>



<details>
<summary >Installation of Python Modules in Ubuntu <a name="Installation_Ubuntu"></a></summary>

In order to run **pyMANGA**, you may need to install modules that are not yet in the **Python** library but are required by pyMANGA.
Since **Python** also plays an important role in the **Ubuntu** operating system, the pre-installed library is very extensive.
Therefore, it is recommended to install the program first and to install any missing modules after the first execution of the program - **pyMANGA** will tell you which modules are needed.

If **pyMANGA** cannot yet be executed due to missing modules in the local Python library - as mentioned at the beginning - one of the missing packages is displayed in an error message.
For the installation of **Python modules**, **pip** ("Pip installs Python") is suitable.
By opening a terminal window (key combination **Ctrl + Alt + T**) and entering the command

	sudo apt-get install python3-pip

pip can be installed.

To add a **Python module** to the library with **pip** the following command must be entered into a terminal:

	pip3 install name_of_the_module

If no manual changes have been made to the standard Python library, the modules "numpy", "vtk", "lxml" and "matplotlib" are missing to run **pyMANGA**.
These must all be installed, so the first command would look like this for the module "numpy":

	pip3 install numpy

The only exception is the module "vtk".
In order to be able to perform calculations with pyMANGA at a later time, which also take the **groundwater flow** into account, **a certain version** is required for this module.
If you do not want to install the latest version of a module with pip, the command looks like this:

	pip3 install vtk==8.1.2

After the missing module is installed, restart **pyMANGA**.
If any other **Python modules** are missing now, **pyMANGA** will again output one of them as missing prerequisite.
Repeat this step until all **Python modules** are installed.
If this is the case, you should get the following output:


	Traceback (most recent call last):
	  File "MANGA.py", line 26, in main
	    prj = XMLtoProject(xml_project_file=project_file)
	UnboundLocalError: local variable 'project_file' referenced before assignment
	
	During handling of the above exception, another exception occurred:
	
	Traceback (most recent call last):
	  File "MANGA.py", line 38, in <module>
	    main(sys.argv[1:])
	  File "MANGA.py", line 28, in main
	    raise UnboundLocalError('Wrong usage of pyMANGA. Type "python' +
	UnboundLocalError: Wrong usage of pyMANGA. Type "python MANGA.py -h" for additional help.


Even if you get this error message first, it means that **pyMANGA** is installed and works correctly.
The calculation of a first example setup is explained in the section  <a href="/docs/getting_started/first_applications_of_pymanga/">First Applications of **pyMANGA**</a> of this short tutorial.

</details>

### Windows

<details>
<summary>Installation of Python in Windows</summary>

To run **pyMANGA**, you must first obtain an **interpreter** for the **Python** programming language.
An example would be **python<sup>T</sup><sup>M</sup>**.
To do this, open your browser and go to ***Python.org***.
In the drop-down menu under ***Download*** you will find the current release version for your operating system of **Python** (this manual describes the procedure for Windows, see <a href="/docs/getting_started/installation/#Figure_1">Figure 1</a>).

<figure class="alert">
     <img id="Figure_1" src="/pictures/getting_started/installation_of_pymanga/download_python_windows_1.jpg">
</figure>

<figure class="alert">
     <img id="Figure_2" src="/pictures/getting_started/installation_of_pymanga/download_python_windows_2.jpg">
</figure>

Execute the downloaded file (***python-3.7.7-amd64.exe***) like a normal Windows exe and install it on your computer (see <a href="/docs/getting_started/installation/#Figure_3">Figure 3</a>). 

<figure class="alert">
     <img id="Figure_3" src="/pictures/getting_started/installation_of_pymanga/installation_python_windows.jpg">
</figure>

This completes the **Python** installation. 
<!-- To start **pyMANGA** some additional preparations have to be made. Go to the subdirectory Preparation and select the appropriate file before your operating system. -->

</details>

<details>
<summary >Installation of Python Modules in Windows <a name="Installation_Ubuntu"></a></summary>

To install python modules, we use the **"Command Prompt"**.
You can easily find it by typing **"Command Prompt"** in the windows search window and opening it with a **mouse click**.
Since pyMANGA is a command line program, everything happens at the command prompt (see <a href="/docs/getting_started/installation/#Figure_5">Figure 5</a>).

<figure class="alert">
     <img id="Figure_4" src="/pictures/getting_started/installation_of_pymanga/open_command_prompt.jpg">
</figure>

Now the following modules ***numpy***, ***vtk***, ***lxml*** and ***matplotlib*** must be installed.
We start with the **module** ***numpy***.
Type the code shown in the **prompt** to install the **module** (see <a href="/docs/getting_started/installation/#Figure_6">Figure 6</a>).

	py -3.7 -m pip install numpy

<figure class="alert">
     <img id="Figure_5" src="/pictures/getting_started/installation_of_pymanga/install_numpy_windows.jpg">
</figure>

Do the same for the other three **modules** with the following code

	py -3.7 -m pip install vtk
	py -3.7 -m pip install lxml
	py -3.7 -m pip install matplotlib

Note: If the prompt says that ***pip*** is not up-to-date, you can use **upgrade** ***pip*** to update it.
However, this is not mandatory.

Some explenations: ***py*** means you are calling **Python**. 
Where **-3.7** is the version you are using.
***-m*** means you are calling a module, in this case ***pip***, which is used to install other **modules**.
Finally, the **module** **name** of the **module** to be installed follows.
Now the preparations for using the **compiler** are finished.


</details>

## Install pyMANGA

After you have set up **Python** on your computer, the next step is to install **pyMANGA**.
You can do this either by cloning the [git-repositories](https://github.com/jbathmann/pyMANGA/ "https://github.com/jbathmann/pyMANGA/") (for advanced users) or by following the instructions below.

The current version of **pyMANGA** can be found on this [homepage](https://github.com/jbathmann/pyMANGA/ "https://github.com/jbathmann/pyMANGA/").
Download the source code of the program as shown in <a href="/docs/getting_started/installation/#Figure_4">Figure 4</a> as zip file.

<figure class="alert">
     <img id="Figure_6" src="/pictures/getting_started/installation_of_pymanga/download_pymanga_ubuntu.png">
</figure>

This zip file must now be unpacked to any location.
Make sure that there are no spaces and no umlauts (like ä,ö,ü,ß) in the file path.
This folder contains all the program components of **pyMANGA**, including ***MANGA.py***, which is the execution file that must be called to execute the program.
Furthermore, the folder contains a collection of benchmarks.

The execution of **pyMANGA** is platform dependent, too.

<details>
<summary >pyMANGA execution in Ubuntu <a name="Installation_Ubuntu"></a></summary>

Open a terminal window with the key combination **Ctrl + Alt + T** and navigate to the main level of the program.
Alternatively, you can also choose the graphical way by navigating to the location via Files.
There you can open the console by right-clicking and in the menu that opens, you have to use the field "Open in Terminal" to open a terminal window, where you are already in the main level of the program.

By typing 

	python3 MANGA.py

the program will be started.

</details>


<details>
<summary>pyMANGA execution in Windows</summary>

To execute pyMANGA, open the pyMANGA directory and **right-click** in an empty area of the **folder** to open the command **prompt** (see <a href="/docs/getting_started/installation/#Figure_5">Figure 5</a>) and enter the following code.

	py MANGA.py -h

Again, ***py*** means Python is called, ***MANGA.py*** represents the file to be called, and ***-h*** calls the help.

<figure class="alert">
     <img id="Figure_7" src="/pictures/getting_started/installation_of_pymanga/open_command_prompt_folder.jpg">
</figure>

Note: The command **prompt** is called in the **folder** so that the **folder path** does not have to be entered each time.
On Windows 10, this is only possible by downloading ***cmd add to context menu.zip*** from the following [web page](https://www.giga.de/downloads/windows-10/tipps/windows-10-wieder-die-eingabeaufforderung-im-kontextmenue-anzeigen/ "https://www.giga.de/downloads/windows-10/tipps/windows-10-wieder-die- prompt in-context menu-display/") and running it as described on the page.
Alternatively, you can use Command **Prompt**, which you can find in Windows **Search** with the search term **"Command Prompt"**, and specify the complete file path, which in this example is ***C:\Users\...\Desktop\pyMANGA-master***.
To find your file path, **right-click** on the ***pyMANGA-master*** **folder** and go to **Properties**.
Here you will find the information about the location of the folder to which you have to add a \ to the **name** of the **folder**

</details>
      
