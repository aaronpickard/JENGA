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

Feature complete

### Functions in block.py

__init__(self): creates a block object

set_block_length(self, n): allows the user to adjust brick length 

set_block_height(self, n): allows the user to adjust brick height

set_block_width(self, n): allows the user to adjust brick width

set_pt1_l_offset(self, n): allows the user to set the point of attachment point 1's length offset

set_pt1_w_offset(self, n): allows the user to set the point of attachment point 1's width offset

set_pt2_l_offset(self, n): allows the user to set the point of attachment point 2's length offset

set_pt2_w_offset(self, n): allows the user to set the point of attachment point 2's width offset

## gcode.py
This file facilitates the printing of the various statements that will move the balloon assembly. These statements will be written in gcode, as a project member has significant experience working in it and with motors that use it. The functions in here will directly control the motion of the balloon assembly.

Feature complete. I am working to make a couple functions operational because they produce output that looks strange, but I think I should be able to do everything that the project requires based on the functions defined here.

### Functions in gcode.py

__init__(self): creates a gcode object

set_neutral(self): sets the neutral point, where the balloon assembly should rest when not in use

set_pickup_point(self): sets the pickup point, where the balloon assembly picks up new bricks (NOTE the functions here assume that all bricks will be picked up in the same location and in the same orientation)

set_placement_point(self): sets the point where the brick is to be place

set_goto_point(self, a, b, c): changing this point allows the user to change the neutral, pickup, and placement points, which can only be changed by setting the goto point

set_feed_rate(self, f): sets the feed rate, which I think is in mm/s

set_units(self): sets the units of the system to mm (gcode works in mm or inches but our bricks are built to mm specification, 50mm x 25mm x 25mm (which is roughly 2in x 1in x 1in, but mm is more precise)

set_separation_height(self, h): allows the user to set the height of the initial vertical climb and final terminal descent of the brick, between which the brick will travel a more optimized path

set_step_size(self, s): allows the user to set the size of steps for functions that move the brick in steps (all functions that move the brick do so in steps)

pickup_brick(self, place): picks up a brick

putdown_brick(self, place): puts down a brick

move_brick_to_placement(self, start, stop): after the brick has been picked up, this function calls helper functions that vertically maneuver the brick, and that move it to the destination point; start and stop are [x,y,z] lists here and throughout this README file

move_parabola_xz(self, start, stop): moves the brick along parabolic arc in the xz frame

move_parabola_yz(self, start, stop): moves the brick along parabolic arc in the yz frame

move_parabola_xyz(self, start, stop): sequentially calls move_parabola_xz() and move_parabola_yz(); NOT OPERATIONAL FUNCTION

make_parabola(self, x1, y1, x2, y2, x3, y3, static_var, static_val): constructs a parabola based on the data passed to it from one of the above three functions (the third point is defined parametrically based on the first two points) and sends it to the printing function

move_vertical(self, start, h): vertically moves a brick, generally the size of the separation height, and called immediately after picking up the brick or immediately before putting it down

move_horizontal(self, start, stop): function that allows the brick to move between two points by breaking down the best way to get there into a unit vector and then multiplying that by some constant so that the balloon moves the step size every step; NOT OPERATIONAL FUNCTION

print_command(self, position_list): converts motion commands to pick up, bring the brick to a set [x, y, z] location, and put it down to gcode, and prints them both to the terminal and to an output file

## main.py
This is the file that one day soon will bring all of these other files together and produce a meaningful gcode instruction set for the balloon assembly to execute.

I think that main.py is feature complete at this point.

### Functions in main.py

This file contains no functions.

## my_utils.py
This is the file where I am throwing any miscellaneous functions I determine that I need but may not belong in a particular class, or may need to be used in multiple classes.

It is a work in progress at this point, and may undergo significant changes throughout the project.

### Functions in my_utils.py

in_to_mm(input): takes an inches value and converts it to mm

get_x_val(): allows user to access an x value in the algorithm system; NOT OPERATIONAL

get_y_val(): allows user to access a y value in the algorithm system; NOT OPERATIONAL

get_z_val(): allows user to access a z value in the algorithm system; NOT OPERATIONAL

## path_to_wall.py
In this file, I am attempting to plan an efficient path to construct a structure (at this point the structure is a simple wall, though that may change after I make progress in these files). Initially, I will attempt to create a simple, somewhat efficient, algorithm to construct a wall with the given hardware architecture.

If all my other, more necessary, contributions to Project JENGA are completed, I may attempt to implement an optimized path planning algorithm, along the lines of what Correll, et al. suggest in their 2013 paper "Assembly Path Planning for Stable Robotic Construction" (http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.1013.2520&rep=rep1&type=pdf).

The initial path to construct the wall is complete. More testing is required to determine which of the various functional and non-functional motion functions I am working on is the most efficient in terms of assembling a wall using the fewest gcode instructions, and in verifying that my basic algorithm can in fact construct a wall. The reach goal of really optimizing the construction path is not complete.

### Functions in path_to_wall.py

Within the Basic(object) class

__init__(self): creates a Basic path object
    
load_pickup(self, x, y, z): interfaces with gcode to adjust the pickup point
    
load_putdown(self, x, y, z): interfaces with gcode to adjust the putdown point
    
load_neutral(self, x, y, z): interfaces with gcode to adjust the neutral point
    
algo(self): assembly algorithm

Within the Fancy(object class:

__init__(self): creates a Fancy path object
    
algo(self, g, σ_limit): implements the algorithm described in "Assembly Path Planning for Stable Robotic Construction"; NOT OPERATIONAL
    
backtrack(self): helper function for the algorithm; NOT OPERATIONAL
