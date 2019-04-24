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
# import gcode
import path_to_wall

my_block = block.Block()
# my_gcode = gcode.GCode()
my_path = path_to_wall.Basic()
my_path.algo2()
my_utils.find_max_z_value('output_instructions.csv')
my_utils.find_illegal_tether_length('output_instructions.csv', 2250)
my_utils.show_path()
my_utils.show_putdown_points()

#block pickup location
