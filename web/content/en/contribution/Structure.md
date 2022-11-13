
---
title: Structure
linkTitle: Structure
weight: 1

---

## Structure

On this page, we provide a brief overview on the structure of the pyMANGA platform.
pyMANGA is composed of different libraries (<a href="/contribution/#Figure_1">Figure 1</a>), each covering a part of the full forest (vegetation) growth model.
This includes, for example, the distribution of individuals ('PopulationLib'), the time step management ('TimeLoopLib') or the growth of individuals ('TreeModelLib').
A library can contain several concepts to describe this specific aspect of the model in different ways.
As pyMANGA follows object-oriented programming paradigms, each concept is defined by a class.
Classes can be inherited to create new concepts.
In some libraries an abstract parent class exists. 
This class is never initiated but serves as a template for all other concepts.
This is, for example, the case in the libraries 'TreeOutputLib' and 'TreeModelLib'.
The documentation of each class can be found [here](https://jbathmann.github.io/pyMANGA/annotated.html).


<figure class="alert">
    <img id="Figure_1" src="/pictures/contribution/manga_structure.png">
    <figcaption>
        <i><br><strong>Figure 1:</strong> Overview on pyMANGA structure. Each grey box represents a library.</i>
    </figcaption>
</figure><p>

The following sections briefly describe each library.


### ProjectLib

This Library manages the interaction of all the other implemented libraries.

### TimeLoopLib

The TimeLoopLib provides functionalities for model timestepping.
Here, the scheduling of sub-models within one time step is defined.

### PopulationLib

In the PopulationLib, the management of individuals within the model is controlled.

### TreeModelLib

The TreeModelLib latter is the heart of pyMANGA as it describes vegetation growth and interaction between individuals and the environment.
A TreeModel always consists of three interacting sub-libraries. 
Those libraries model the gathering of resources, above- and below-ground, as well as vegetation growth.
The communication between those libraries is managed by interfaces. 

#### AbovegroundCompetition

This sub-library characterizes the gathering of resources available above the ground.
An above-ground resource relevant to pyMANGA is sunlight availability.
A sub-model can, for example, describe how sunlight is available to individual trees if they are shwadowd by others.

#### BelowgroundCompetition

This sub-library characterizes the resource gathering below the ground.
Since pyMANGA models growth via the presence of resources, these are also the focus of this submodel.
The below-ground resource relevant to pyMANGA con for example represent the nutrient availability.

#### TreeGrowthAndDeath

In the third and last main sub-library of the TreeModelLib, the dynamic concept of tree (vegetation) growth and death is described.

### TreeOutputLib

The TreeOutputLib controls the way pyMANGA generates output files from the simulation results.

### VisualizationLib

The VisualizationLib defines an interface for the visualization of model results during runtime.

