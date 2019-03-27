# Project JENGA
Project JENGA code repository.

# Project Overview
Project JENGA (Just Everything Needed for Ground Architecture) is a a final project in the Spring 2019 semester of MEIE 4810 Introduction to Human Spaceflight, which is being taught at Columbia University by Professor Michael Massimino. The objective of Project JENGA is to design an architecture to take bricks made of Martian regolith (the composition and creation of the bricks is out of the scope of the project) and use it to create a useful structure. Then we will prototype the architecture in Earth conditions, bringing it to Technology Readiness Level (TRL) 5. 

Our technique involves using a black body balloon (which we will likely simulate using one or several helium balloons tied together) to generate buoyancy in the Martian atmosphere. The balloon will be connected via tether to four base stations spread out at equal distances and angles from each other. The balloon will be maneuvered over the construction site by varying the lengths of the tethers.
This repo is the site of the software developed for the project.

# Project Participants
Aaron Pickard, Albert Tai, Chris Fryer, Thomas Orr, Victoria Wang

# Python Files
## block.py
This file defines the notional brick we are using to build our structures and validate our architecture. Presently, each brick is 50mm x 25mm x 25mm, has two pyramid-shaped notches on top with bases of 25mm x 25mm to aid in construction, and is a hollow shell of 3D-printed plastic. The file defines the shape of the block in three dimensions, as well as the offsets necessary for the architecture to pick up and place the block appropriately using electromagnets and functions that can be used to adjust these values.

I think it is feature complete at this point, and hope to describe the functions in the file the next time I edit this README.

### Functions in block.py
Placeholder.

## gcode.py
This file facilitates the printing of the various statements that will move the balloon assembly. These statements will be written in gcode, as a project member has significant experience working in it and with motors that use it. The functions in here will directly control the motion of the balloon assembly.

It is a work in progress at this point. Finishing this file in particular is my priority over the next couple of weeks.

### Functions in gcode.py
Placeholder.

## main.py
This is the file that one day soon will bring all of these other files together and produce a meaningful gcode instruction set for the balloon assembly to execute.

It is a work in progress at this point, and will undergo significant changes throughout the project.

### Functions in main.py
Placeholder.

## my_utils.py
This is the file where I am throwing any miscellaneous functions I determine that I need but may not belong in a particular class, or may need to be used in multiple classes.

It is a work in progress at this point, and may undergo significant changes throughout the project.

### Functions in my_utils.py
Placeholder.

## path_to_wall.py
In this file, I am attempting to plan an efficient path to construct a structure (at this point the structure is a simple wall, though that may change after I make progress in these files). Initially, I will attempt to create a simple, somewhat efficient, algorithm to construct a wall with the given hardware architecture.

If all my other, more necessary, contributions to Project JENGA are completed, I may attempt to implement an optimized path planning algorithm, along the lines of what Correll, et al. suggest in their 2013 paper "Assembly Path Planning for Stable Robotic Construction" (http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.1013.2520&rep=rep1&type=pdf).

It is a work in progress at this point, and may undergo significant changes throughout the project.

### Functions in path_to_wall.py
Placeholder
