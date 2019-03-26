"""
Aaron Pickard
ajp2235
Spring 2019
main.py
This file controls the generation of a gcode instruction set for Project JENGA.
This file supports Project JENGA, a final project in the Spring 2019 semester of
MEIE 4810 Introduction to Human Spaceflight at Columbia University.
"""

import block
import my_utils
import gcode

my_block = block.Block()
my_gcode = gcode.GCode()

#define block parameters
my_gcode.set_units()
my_block.block_l = 50
my_block.block_w = 25
my_block.block_h = 25


#block pickup location

def user_defined_block_pickup():
    #for instances where I want the user to do it