---
title: "First applications of pyMANGA"
linkTitle: "First applications of pyMANGA"
weight: 2
description:
---

<head>
<style type="text/css">
<!--
details summary {color: white; background: #00305E; margin-bottom: 1em;}
-->
</style>
</head>

Before you start with first applications, if you haven't already done so, you should read the <a href="/docs/getting_started/installation">installation and preparation instructions</a> for your operating system. This is especially recommended for beginners who have little experience with **Python** and the input console. These instructions are generally suitable for all three operating systems (MacOS, Unbunt, Windows). The following chapter is described based on the execution in Windows. Note the corresponding changes when using Ubuntu (e.g. no backslashes, "python" instead of "py" in terminal, etc.)

## Simple sample setups without OpenGeoSys

First you have to use the console interface again to navigate to the file location of the **pyMANGA** main level. Entering then for **Windows**

	• py main.py -h  			         [1a]

respectively for **Ubuntu**

	• python main.py -h  			         [1b]

starts **pyMANGA** and displays all available input options (-h stands for help).

<figure>
<a name="Figure_1"></a>
<img src="/pictures/ausgefuehrte_main_py_Datei_in_der_Eingabekonsole.jpg">
<figcaption><font size = "1"><i><b>Figure 1: </b>Executed main.py file in the windows input console.</i></font></figcaption>
</figure><p>

Here you can see that the ***main.py*** file has been executed and is waiting for further input. So the start of **pyMANGA** was successful and you can test some first usage examples. You can enter the following code (see <a href="/docs/getting_started/first_applications_of_pymanga/#Figure_2">Figure 2</a>) for **Windows**:

	• py main.py -i test\SmallTests\Test_Setups_small\AllSimple_WithOutput.xml	    		 [2a]

respectively for **Ubuntu**:

	• python main.py -i test/SmallTests/Test_Setups_small/AllSimple_WithOutput.xml	    		 [2b]

***-i*** refers to the index or path of the file in which the input to be used for this example is defined. Note that the use of backslashes in the file path only applies to the Windows variant.

<figure>
<a name="Figure_2"></a>
<img src="/pictures/Fehlermeldung_beim_Aufuehren_von_py-main.py.jpg">
<figcaption><font size = "1"><i><b>Figure 2:</b> Error message when trying to <b>py main.py -i .\test\SmallTests\Test_Setups_small\AllSimple_WithOutput.xml.</b></i></font></figcaption>
</figure><p>

After executing the code, an error message is displayed, which describes that a folder named ***testoutputs*** does not exist, but is needed by the program to save the simulation results. This information can be found in the file ***AllSimple_WithOutput.xml***, which defines the input for our example. To view it, you have to open the file using the editor. You will find the file under the following path: 

***.\test\SmallTests\Test_Setups_small\AllSimple_WithOutput.xml***

To do so, please create the directory which is listed in the xml-file. The default settings for the file path is: 

***test\testoutputs***


The specified file path is relative to the folder where you started pyMANGA. Right-click on the file, click ***Open with*** and select the editor (see <a href="/docs/getting_started/first_applications_of_pymanga/#Figure_3">Figure 3</a>).

<figure>
<a name="Figure_3"></a>
<img src="/pictures/Inhalt_von_AllSimple_WithOutput.xml,_geoeffnet_mit_dem_Text_Editor.jpg">
<figcaption><font size = "1"><i><b>Figure 3:</b> Content of </b>AllSimple_WithOutput.xml</b>, opened with the Text Editor.</i></font></figcaption>
</figure><p>

The file contains the **red-marked** lines, which define the programs output, e.g. the **tree height (h_stem)** and where to put it, namely in the non-existent folder ***testoutputs***, which was defined as the output location for the simulation results. Consequently, you must now create this folder. To do this, right-click in the subfolder ***C:\Users\chris\Desktop\pyMANGA-master\test***, click on Create new folder and name it testoutputs (see <a href="/docs/getting_started/first_applications_of_pymanga/#Figure_4">Figure 4</a>).

<figure>
<a name="Figure_4"></a>
<img src="/pictures/Erstellung_des_neuen_Ordners_testoutputs.jpg">
<figcaption><font size = "1"><i><b>Figure 4:</b> Creating the new folder <b>testoutputst</b>.</i></font></figcaption>
</figure><p>

Then run code 1 again at the command prompt. Now the program should start the first simulation (see <a href="/docs/getting_started/first_applications_of_pymanga/#Figure_5">Figure 5</a>). There are several input parameters which can be set in MANGA project configurations. The file which has just been started is a configuration file. A description of these parameters can be found on the following [website](https://jbathmann.github.io/pyMANGA/project_dox__MangaProject__MangaProject.html "https://jbathmann.github.io/pyMANGA/project_dox__MangaProject__MangaProject.html").The results of the simulation are displayed once visually in a separate window (see <a href="/docs/getting_started/first_applications_of_pymanga/#Figure_6">Figure 6</a>) and in the form of ***csv*** files in the newly created folder ***testoutputs***. You have successfully executed the first example.

<figure>
<a name="Figure_5"></a>
<img src="/pictures/Widerholte_Ausfuehrung_von_py_main.py_-i_ProjectLibExampleSetupsAllSimple_WithOutput.xml_nach_erstellung_den_neuen_Ordner_testoutputs.jpg">
<figcaption><font size = "1"><i><b>Figure 5:</b> Repeated performance of  <b>py main.py -i ProjectLib\ExampleSetups\AllSimple_WithOutput.xmlt</b> After creating the new folder  <b>testoutputst</b>.</i></font></figcaption>
</figure><p>

<figure>
<a name="Figure_6"></a>
<img src="/pictures/Visuelle_Ergebnisse_der_Simulation.jpg">
<figcaption><font size = "1"><i><b>Figure 6:</b> Visual results of the simulation.</i></font></figcaption>
</figure><p>

Similarly, you can use the following codes to try out two more examples where other input variants are defined. However, you must first empty the ***testoutputs*** folder or define another folder in the input files using the editor, since the program cannot overwrite the old output data. Then enter the code in the command prompt again. In addition, other parameters were changed again. Use the [website](https://jbathmann.github.io/pyMANGA/project_dox__MangaProject__MangaProject.html "https://jbathmann.github.io/pyMANGA/project_dox__MangaProject__MangaProject.html") to get an overview of the setting variants of the input parameters used in the examples and compare them. 

	• py main.py -i \test\SmallTests\Test_Setups_small\FIXEDSAL_BETTINA.xml   [3] 
	• py main.py -i \test\SmallTests\Test_Setups_small\FON_SAZOI_KIWI.xml     [4]

Due to other project configurations (in ***FIXEDSAL_BETTINA.xml and FON_SAZOI_KIWI.xml***) there is no visual representation in the code 3 example (compare <a href="/docs/getting_started/first_applications_of_pymanga/#Figure_4">Figure 6</a>).

## More complex sample setups with OpenGeoSys


The next application of **pyMANGA** uses **OpenGeoSys** (OGS). This is a scientific open source project for the development of numerical methods for the simulation of thermo-hydro-mechanical-chemical (THMC) processes in porous and fragmented media. To use **OGS** you must first download and install it. Since the installation is very different between the operating systems, the following explanation is individually formulated for your operating system.


<details>
<summary >First applications of pyMANGA with OGS in Ubuntu</summary>
<p>
Here you will soon find a description for Ubuntu. Please feel free to have a look at the already existing content for Windows.
</p>
</details>

<details>
<summary>First applications of pyMANGA with OGS in Windows</summary>
<p>

To use **OGS** you have to download and install it first. To do so, go to the following [website](https://www.opengeosys.org/releases/ "https://www.opengeosys.org/releases/") and scroll down until you find **version 6.3.0** and download it (see <a href="/docs/getting_started/first_applications_of_pymanga/#Figure_7">Figure 7</a> and <a href="/docs/getting_started/first_applications_of_pymanga/#Figure_8">Figure 8</a>).


<figure>
<a name="Figure_7"></a>
<img src="/pictures/Versionsauswahl_von_OGS.jpg">
<figcaption><font size = "1"><i><b>Figure 7:</b> Version selection of OGS.</i></font></figcaption>
</figure><p>

<figure>
<a name="Figure_8"></a>
<img src="/pictures/Download_von_OGS 6.3.0.jpg">
<figcaption><font size = "1"><i><b>Figure 8:</b> Download OGS 6.3.0.</i></font></figcaption>
</figure><p>

Select the file to be downloaded according to your operating system.  Then unzip the zip file, copy the ***bin*** folder and paste it into the ***pyMANGA-master*** folder in the following path (see <a href="/docs/getting_started/first_applications_of_pymanga/#Figure_9">Figure 9</a>).

	• pyMANGA-master\TreeModelLib\BelowgroundCompetition\OGS					 [5]

<figure>
<a name="Figure_9"></a>
<img src="/pictures/Einfuegen_von_OGS_in_den_pyMANGA-master_Ordner.jpg">
<figcaption><font size = "1"><i><b>Figure 9:</b> Insert OGS into the pyMANGA-master folder.</i></font></figcaption>
</figure><p>

**OGS** is now installed. To test if it works properly, open the ***_Bin_*** folder, press **shift** and the **right mouse button** and select **Open PowerShell window here** (see Figure <a href="/docs/getting_started/first_applications_of_pymanga/#Figure_10">Figure 10</a>).

<figure>
<a name="Figure_10"></a>
<img src="/pictures/Test_ob_OGS_Ordnungsgemaeß_funktioniert.jpg">
<figcaption><font size = "1"><i><b>Figure 10:</b> Test if OGS works properly.</i></font></figcaption>
</figure><p>

Copy the path that appears in the **PowerShell window** and append ***\OGS*** and press Enter. The following <a href="/docs/getting_started/first_applications_of_pymanga/#Figure_11">Figure 11</a> shows the PowerShell window output when OGS is running smoothly. 

<figure>
<a name="Figure_11"></a>
<img src="/pictures/Ausgabe_bei_Ordnungsgemaeßer_Funktion_von_OGS.jpg">
<figcaption><font size = "1"><i><b> Figure 11:</b> Output if OGS functions properly.</i></font></figcaption>
</figure><p>

Now you can start the next application example by opening the command prompt in the ***pyMANGA-master*** folder and starting pyMANGA as usual. Then enter the following command (see <a href="/docs/getting_started/first_applications_of_pymanga/#Figure_12">Figure 12</a>).

	• py main.py -i \test\LargeTests\Test_Setups_large\OGS3D_SAZOI_BETTINA.xml 				 [6]

<figure>
<a name="Figure_12"></a>
<img src="/pictures/zeigt_die_Ausfuehrung_des_Anwendungsbeispiels_mit_OGS.jpg">
<figcaption><font size = "1"><i><b>Figure 12:</b> shows the execution of the application example with OGS.</i></font></figcaption>
</figure><p>

Note: The computing time can take several hours. You can reduce this by opening 

***test\LargeTests\Test_Setups_large\OGS3D_SAZOI_BETTINA.xml*** 

and adding the following line

	• <delta_t_ogs> 604800 </delta_t_ogs>							 [7]

Here **604800** is given in seconds and can be varied. Here, it corresponds here to one week, i.e. the ogs-calculations are not performed for the home timestep in the tree model but only for one week. From the results the porewater distribution is extrapolated under steady state assumptions. Consequently, this parameter has to be used very carefully but is a means to significantly reduce computing time (see <a href="/docs/getting_started/first_applications_of_pymanga/#Figure_13">Figure 13</a>).

<figure>
<a name="Figure_13"></a>
<img src="/pictures/Anpassung_zur_Rechenzeit_Verkuerzung.jpg">
<figcaption><font size = "1"><i><b>Figure 13:</b> Adaptation to the computing time reduction.</i></font></figcaption>
</figure><p>

</p>
</details>

