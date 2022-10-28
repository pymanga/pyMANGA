
---
title: Structure
linkTitle: Structure
weight: 1

---

On this page, we provide a brief overview on the structure of the pyMANGA platform.
pyMANGA is composed of different libraries (<a href="/contribution/#Figure_1">Figure 1a</a>), each covering a part of the full forest (vegetation) growth model.
This includes, for example, the distribution of individuals ('PopulationLib'), the time step management ('TimeLoopLib') or the growth of individuals ('TreeModelLib').
A library can contain several concepts to describe this specific aspect of the model in different ways.
As pyMANGA follows object-oriented programming paradigms, each concept is defined by a class.
Classes can be inherited to create new concepts.
In some libraries an abstract parent class exists. 
This class is never initiated but serves as a template for all other concepts.
This is, for example, the case in the libraries 'TreeOutputLib' and 'TreeModelLib'.
The documentation of each class can be found [here](https://jbathmann.github.io/pyMANGA/annotated.html).


<figure class="alert">
    <img id="Figure_1" src="/pictures/contribution/manga_structure.jpg">
    <figcaption>
        <i><br><strong>Figure 1:</strong> Overview on pyMANGA structure. Each grey box represents a library.</i>
    </figcaption>
</figure><p>

The following sections briefly describe each library.


### ProjectLib

- initiate a simulation based on the project file

### TimeLoopLib
### PopulationLib
### TreeModelLib

The 'TreeModelLib' latter is the heart of pyMANGA as it describes vegetation growth and interaction between individuals and the environment.

### TreeOutputLib
### VisualizationLib

