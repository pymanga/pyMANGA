---
title: "First applications of pyMANGA"
linkTitle: "First applications of pyMANGA"
weight: 3
description:
---
Before you start with the first applications, if you haven't already done so, you should read the installation and preparation instructions for your operating system, this is recommended especially for beginners who have little experience with Python and the input console. These instructions are suitable for all three operating systems (MacOS, Unbunt, Windows), if there are any special features in the execution on the respective systems, please refer to the notes.   

<figure>
<img src="/de/static/ausgefuehrte_main_py_Datei_in_der_Eingabekonsole.jpg">
<figcaption><font size = "1"><i><b>Figure 1:</b>Executed main.py file in the input console.</i></font></figcaption>
</figure><p>

Here you can see that the *main.py* file has been executed and is waiting for further input. So the start of MANGA was successful and you can test some first usage examples. You can enter the following code (see figure 2).

	• py main.py -i ProjectLib\ExampleSetups\AllSimple_WithOutput.xml	    [1]

*-i* describes the index or path of the file in which the input to be used for this example is defined.   

<figure>
<img src="/de/static/Fehlermeldung_beim_Aufuehren_von_py-main.py.jpg">
<figcaption><font size = "1"><i><b>Figure 2:</b> Error message when trying to <b>py main.py -i ProjectLib\ExampleSetups\AllSimple_WithOutput.xml.</b></i></font></figcaption>
</figure><p>

After executing the code, an error message is displayed, which describes that a folder named *testoutputs* does not exist, but is needed by the program to save the generated data of the simulation. This information can be found in the file *AllSimple_WithOutput.xml*, which defines the input for our example. To view it, you have to open the file using the editor. To do so, please create the directory listed (see figure 2). The specified file path is relative to the folder where you started pyMANGA, see figure 3. To do this, follow the file path in the *pyMANGA-master* folder as shown in Figure 2, right-click on the file, click *Open with* and select the editor (see Figure 3).

<figure>
<img src="/de/static/Inhalt_von_AllSimple_WithOutput.xml,_geoeffnet_mit_dem_Text_Editor.jpg">
<figcaption><font size = "1"><i><b>Figure 3:</b> Content of </b>AllSimple_WithOutput.xml</b>, opened with the Text Editor.</i></font></figcaption>
</figure><p>

The file contains the red-marked lines, which indicate what is to be output by the program, e.g. the tree height (h_stem) and where to put it, namely in the non-existent folder *testoutputs*, which was defined as the output location for the simulation results. Consequently, you must now create this folder. To do this, right-click in the subfolder *C:\Users\chris\Desktop\pyMANGA-master\ProjectLib\ExampleSetups*, click on Create new folder and name it testoutputs (see Figure 4).

<figure>
<img src="/de/static/Erstellung_des_neuen_Ordners_testoutputs.jpg">
<figcaption><font size = "1"><i><b>Figure 4:</b> Creating the new folder <b>testoutputst</b>.</i></font></figcaption>
</figure><p>

Then run code 1 again at the command prompt. Now the program should start the first simulation (see figure 5). There are several input parameters which can be set in MANGA project configurations. The file which has just been started is a configuration file. A description of these parameters can be found on the following website [Link](https://jbathmann.github.io/pyMANGA/project_dox__MangaProject__MangaProject.html "https://jbathmann.github.io/pyMANGA/project_dox__MangaProject__MangaProject.html").The results of the simulation are displayed once visually in a separate window (see Figure 6) and in the form of *csv* files in the newly created folder *testoutputs*. You have successfully executed the first example.

<figure>
<img src="/de/static/Widerholte_Ausfuehrung_von_py_main.py_-i_ProjectLibExampleSetupsAllSimple_WithOutput.xml_nach_erstellung_den_neuen_Ordner_testoutputs.jpg">
<figcaption><font size = "1"><i><b>Figure 5:</b> Repeated performance of  <b>py main.py -i ProjectLib\ExampleSetups\AllSimple_WithOutput.xmlt</b> After creating the new folder  <b>testoutputst</b>.</i></font></figcaption>
</figure><p>

<figure>
<a name="Abbildung_6"></a>
<img src="/de/static/Visuelle_Ergebnisse_der_Simulation.jpg">
<figcaption><font size = "1"><i><b>Figure 6:</b> Visual results of the simulation.</i></font></figcaption>
</figure><p>

Similarly, you can use the following codes to try out two more examples where other input variants are defined. However, you must first empty the *testoutputs* folder or define another folder in the input files using the editor, since the program cannot overwrite the old output data. Then enter the code in the command prompt again. In addition, other parameters were changed again. Use the website [Link](https://jbathmann.github.io/pyMANGA/project_dox__MangaProject__MangaProject.html "https://jbathmann.github.io/pyMANGA/project_dox__MangaProject__MangaProject.html") to get an overview of the setting variants of the input parameters used in the examples and compare them. 

	• py main.py -i ProjectLib\ExampleSetups\FIXEDSAL_BETTINA.xml 	            [2] 
	• py main.py -i ProjectLib\ExampleSetups\FON_SAZOI_KIWI.xml	            [3]

Due to other project configurations (in *FIXEDSAL_BETTINA.xml and FON_SAZOI_KIWI.xml*) there is no visual representation in the code 3 example (compare <a href="/en/docs/first_steps/first_applications/first_applications_of_pymanga/#Figure_6">Figure 6</a> ). 