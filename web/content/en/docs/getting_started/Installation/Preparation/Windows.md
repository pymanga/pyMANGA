---
title: "Preparations for starting pyMANGA under Microsoft Windows 10"
linkTitle: "Microsoft Windows"
weight: 3
description: >
---
In order to run MANGA, some modules for the Python compiler must be installed. You have to open the *prompt* for this. You can easily find it by searching for it by typing "Command Prompt" and opening it with a mouse click. Since MANGA is a line program, everything happens at the command prompt (see figure 1).

<figure>
<img src="/pictures/oeffnen_der_Eingabeaufforderung.jpg">
<figcaption><font size = "1"><i><b>Figure 1:</b>open the command prompt.</i></font></figcaption>
</figure><p>

Now the following modules *numpy*, *vtk*, *lxml* and *matplotlib* must be installed. We start with the module *numpy*. Type the code shown in the prompt to install the module (see Figure 2).

	• py -3.7 -m pip install numpy						     		[1]

<figure>
<img src="/pictures/Beispielhafte_Installation_des_Moduls_numpy.jpg">
<figcaption><font size = "1"><i><b>Figure 2:</b> Exemplary installation of the numpy module.</i></font></figcaption>
</figure><p>

Do the same for the other three modules with the following code

	• py -3.7 -m pip install vtk						     		[2]
	• py -3.7 -m pip install lxml					  	     		[3]
	• py -3.7 -m pip install matplotlib					     		[4]

Note: If the prompt says that *pip* is not up to date, you can use upgrade *pip* to update it. However, this is not mandatory.

Some explenations: *py* means you are calling Python. Where -3.7 is the version you are using. *-m* means you are calling a module, in this case *pip*, which is used to install other modules. Finally, the module name of the module to be installed follows. Now the preparations for using the compiler are finished. As a next step you have to download the program MANGA, if you haven't done so already. To do this, go to the following website [Link](https://github.com/jbathmann/pyMANGA/ "https://github.com/jbathmann/pyMANGA/") and download the program as a zip file and save it on your computer (see Figure 3).

<figure>
<img src="/pictures/Download_von_pyMANGA.jpg">
<figcaption><font size = "1"><i><b>Figure 3:</b> Download from pyMANGA.</i></font></figcaption>
</figure><p>

Then unzip the file (*pyMANGA-master.zip*) to your desktop. It contains all the program components of MANGA, including *main.py*, which is the execution file that must be called to execute the program. To do so, open the folder and right-click in an empty area of the folder to open the command prompt (see Figure 4) and enter the following code.

	• py main.py -h								     		[5]

Again, *py* means Python is called, *main.py* represents the file to be called, and -h calls the help.   

<figure>
<img src="/pictures/oeffnen_der_Eingabeaufforderung_im_pyMANGA_Ordner.jpg">
<figcaption><font size = "1"><i><b>Figure 4:</b> open the command prompt in the pyMANGA folder.</i></font></figcaption>
</figure><p>

Note: The command prompt is called in the folder so that the folder path does not have to be entered each time. On Windows 10, this is only possible by downloading *cmd add to context menu.zip* from the following web page [link](https://www.giga.de/downloads/windows-10/tipps/windows-10-wieder-die-eingabeaufforderung-im-kontextmenue-anzeigen/ "https://www.giga.de/downloads/windows-10/tipps/windows-10-wieder-die- prompt in-context menu-display/") and running it as described on the page. Alternatively, you can use Command Prompt, which you can find in Windows Search with the search term "Command Prompt", and specify the complete file path, which in this example is *C:\Users\...\Desktop\pyMANGA-master*. To find your file path, right-click on the *pyMANGA-master* folder and go to Properties. Here you will find the information about the location of the folder to which you have to add a \ to the name of the folder.    
      