
---
title: Style
linkTitle: Style
weight: 2

---

## Most important rules to remember

- Never use global variables.
- Give descriptive names to functions, variables, and file names; avoid abbreviation.
    - Variable names start lowercase and then with underscore (*this_examlpe*). Class member variables start with an underscore., which makes them private (*self._class_variable*).
    - Regular functions or class methods start lowercase and then camel case (*thisExample*).
    - Classes start with uppercase and then camel case (*ThisExample*).
- Define only one class per file.
- Document your code.

## Naming

The most important consistency rules are those that govern naming. The style of a name immediately informs us what sort of thing the named entity is: a type, a variable, a function, a constant, a macro, etc., without requiring us to search for the declaration of that entity. The pattern-matching engine in our brains relies a great deal on these naming rules.

Naming rules are pretty arbitrary, but we feel that consistency is more important than individual preferences in this area, so regardless of whether you find them sensible or not, the rules are the rules.
### General Naming Rules
Function names, variable names, and filenames should be descriptive; eschew abbreviation. Types and variables should be nouns, while functions should be imperative verbs.
#### File Names
Filenames should be camel case and do not include underscores (_) or dashes (-). The name must match the class that is defined in the file.

#### Type Names
Type names start with a capital letter and have a capital letter for each new word, with no underscores: *MyExcitingClass*, *MyExcitingEnum*.
#### Variable Names
Variable names are lowercase names with underscores: *_my_exciting_member_variable*. But be consistent in a file!
#### Function Names
Function names should represent an action. Regular functions start lowercase an then camel case. Accessors and mutators match the name of the variable with a "get" or "set" prefix: *doSomeStuff()*, *doSomeStuffOnThing()*, *getMyExcitingMemberVariable()*, *setMyExcitingMemberVariable()*.

## Comments

Though a pain to write, comments are absolutely vital to keeping our code readable.
The following rules describe what you should comment and where.
But remember: while comments are very important, the best code is self-documenting.
Giving sensible names to types and variables is much better than using obscure names that you must then explain through comments.

When writing your comments, write for your audience: the next contributor who will need to understand your code. Be generous — the next one may be you!
### Comment Style
For comments inside the implementation use the # syntax, as long as you are consistent. For header file comments use Doxygen ### comments. Doxygen allows to automatically generating browsable source code documentation. Additional information like a brief description or function parameter description can be added inside Doxygen comments with backslashed or @-prefixed keywords like /// \brief or /// @see.
#### File Comments
Start each file with the copyright and license notice, followed by a description of the contents of the file.
#### Class Comments
Every class definition should have an accompanying comment that describes what it is for and how it should be used.
#### Function Comments
Declaration comments describe use of the function; comments at the definition of a function describe operation.
#### Variable Comments
In general the actual name of the variable should be descriptive enough to give a good idea of what the variable is used for. In certain cases, more comments are required.
#### Implementation Comments
In your implementation you should have comments in tricky, non-obvious, interesting, or important parts of your code.
#### Punctuation, Spelling and Grammar
Pay attention to punctuation, spelling, and grammar; it is easier to read well-written comments than badly written ones.
#### TODO Comments
Use TODO comments for code that is temporary, a short-term solution, or good-enough but not perfect.
Formatting

Coding style and formatting are pretty arbitrary, but a project is much easier to follow if everyone uses the same style.
Individuals may not agree with every aspect of the formatting rules, and some of the rules may take some getting used to, but it is important that all project contributors follow the style rules so that they can all read and understand everyone's code easily.
We use googles **yapf** Software to automatically follow the 'clang-format'.

## Exceptions to the Rules

The coding conventions described above are mandatory.
However, like all good rules, these sometimes have exceptions, which we discuss here.
You may diverge from the rules when dealing with code that does not conform to this style guide.

Use common sense and BE CONSISTENT.

If you are editing code, take a few minutes to look at the code around you and determine its style.
If they use spaces around their if clauses, you should, too.
If their comments have little boxes of stars around them, make your comments have little boxes of stars around them too.

The point of having style guidelines is to have a common vocabulary of coding so people can concentrate on what you are saying, rather than on how you are saying it.
We present global style rules here so people know the vocabulary.
But local style is also important.
If code you add to a file looks drastically different from the existing code around it, the discontinuity throws readers out of their rhythm when they go to read it.
 Try to avoid this.

OK, enough writing about writing code; the code itself is much more interesting.
Have fun!
