"""
Aaron Pickard
ajp2235
Spring 2019
gcode.py
This file defines gcode operations used to assemble blocks into a structure in Project JENGA.
This file supports Project JENGA, a final project in the Spring 2019 semester of
MEIE 4810 Introduction to Human Spaceflight at Columbia University.
"""

import math

"""
TODO revise assumptions
Assumptions: 
1. The 4 wires in this system are all 2m (2000mm) long. Each wire length is represented by an axis.
2. MOTOR NAMES
3. All default positions until changed are (0,0,0).
4. The pickup position and orientation is the same for every block.
5. Functions that have gcode or mcode output are named with the prefix move_
6. Functions that manipulate variables are named with the prefix set_
7. There are 4 kinds of locations - neutral (resting place), pickup (where bricks are picked up), 
   placement (where bricks are put down), and goto (where a location can be manually edited).
8. Each function that gives output will convert to tether lengths
"""


class GCode(object):
    def __init__(self):
        self.neutral_point = [0, 0, 0] # x,y,z
        self.pickup_point = [0, 0, 0]
        self.placement_point = [0, 0, 0]
        self.goto_point = [0, 0, 0]
        self.ul_base = [-2000, 2000, 0]   # upper left base station coordinates - MOTOR X
        self.ur_base = [2000, 2000, 0]    # upper right base station coordinates - MOTOR Y
        self.ll_base = [-2000, -2000, 0]  # lower left base station coordinates - MOTOR Z
        self.lr_base = [2000, -2000, 0]   # lower right base station coordinates - MOTOR E
        self.ul_base_offset = [0, 0, 0]
        self.ur_base_offset = [0, 0, 0]
        self.ll_base_offset = [0, 0, 0]
        self.lr_base_offset = [0, 0, 0]
        self.feed_rate = 2000
        self.step_size = 10

    def set_neutral(self):
        self.neutral_point = self.goto_point

    def set_pickup_point(self):
        self.pickup_point = self.goto_point

    def set_placement_point(self):
        self.placement_point = self.goto_point

    def set_goto_point(self, a, b, c):
        self.goto_point = [a, b, c]

    def set_feed_rate(self, f):   # feed rate in mm/m
        self.feed_rate = f
        print("G1 F%d ; ") % self.feed_rate

    def set_units(self):
        print("G21 ; This program requires operations with the gcode millemeter setting")

    def move_brick_to_placement(self, start, stop):
        """
        LINEAR INTERPOLATION gcode ALGORITHM (getting to place and from it)
        1 calculate total distance
            a) start at pickup point (likely to be close to z=0
            b) terminal approach to placement is at least 20mm from both pickup and putdown (that terminate at same
               height?) - discretize in segments of 5 mm
            c) third point is midpoint of them + function of the linear distance between them up (if  closer dont go as far up)
            d) find inverse parabola using maths
        2 set variable for max distance between points
        3 int divide(ceiling) total distance by max distance to get step distance
        4 I have to discretize the parabola!!!
        5 last step is conversion to tether lengths
        """

        # Variable declaration
        separation_height = 20
        start_x = start[0]
        start_y = start[1]
        start_z = start[2]
        stop_x = stop[0]
        stop_y = stop[1]
        stop_z = stop[2]
        parabola_stop_z = stop[2] + separation_height
        parabola_stop = [stop_x, stop_y, parabola_stop_z]

        # Motion commands
        self.move_vertical(start, separation_height)
        start[2] += separation_height
        self.move_parabola_xz(start, parabola_stop)
        self.move_parabola_yz(start, parabola_stop)
        self.move_vertical(parabola_stop, (-1*separation_height))

    def move_parabola_xz(self, start, stop):
        #Moves in the xz frame
        start_x = start[0]
        start_z = start[2]
        stop_x = stop[0]
        stop_z = stop[2]
        midpoint_x = (start_x + stop_x) / 2
        midpoint_z = 1.5 * midpoint_x

    def move_vertical(self, start, h):
        """
        1 get current location (x,y,z)
        2 get intermediate end effector positions (x,y,z,p) - p is boolean
        3 iterate through each intermediate position and from that convert to tether length
        """
        height = h
        num_steps = 0
        temp = 0
        start_x = start[0]
        start_y = start[1]
        start_z = start[2]
        stop_z = start_z + height
        intermediate = [start_x, start_y, start_z]
        temp = height/self.step_size
        num_steps = math.ceil(temp)

        while start_z < stop_z:
            #calculate new intermediate position
            intermediate[2] = intermediate[2] + self.step_size
            #convert to change in height & print instruction
            self.print_command(intermediate)
            if stop_z - intermediate[2] < self.step_size:
                #calculate new intermediate position
                intermediate[2] = intermediate[2] + (stop_z - intermediate[2])
                #convert to change in height & print instruction
                self.print_command(intermediate)
                break

    def print_command(self, position_list):
        """
        Special cases
        x = -999 print M8 (pickup) & break
        x = 999 print M9 (putdown) & break
        so I want to print
        x value = sqrt((brick position)^2 + (brick position x offset)^2 - (x position)^2)
        y value = sqrt((brick position)^2 + (brick position y offset)^2 - (y position)^2)
        z value = sqrt((brick position)^2 + (brick position z offset)^2 - (z position)^2)
        e value = sqrt((brick position)^2 + (brick position e offset)^2 - (e position)^2)
        last 2 variables are always the same, middle representing the end effector offset, and last representing the tether base position
        """

        x_pos = position_list[0]
        y_pos = position_list[1]
        z_pos = position_list[2]

        if x_pos == 999:
            # Pickup
            print("M8 ; ")

        elif x_pos == -999:
            # Putdown
            print("M9 ; ")

        else:
            # Motion calculations
            # Upper left base
            x_end_offset = self.ul_base_offset[0]
            y_end_offset = self.ul_base_offset[1]
            z_end_offset = self.ul_base_offset[2]
            x_base_pos = self.ul_base[0]
            y_base_pos = self.ul_base[1]
            z_base_pos = self.ul_base[2]
            temp_x = (x_pos + x_end_offset + x_base_pos) ** 2
            temp_y = (y_pos + y_end_offset + y_base_pos) ** 2
            temp_z = (z_pos + z_end_offset + z_base_pos) ** 2
            ul_output = math.sqrt(temp_x + temp_y + temp_z)

            # Upper right base
            x_end_offset = self.ur_base_offset[0]
            y_end_offset = self.ur_base_offset[1]
            z_end_offset = self.ur_base_offset[2]
            x_base_pos = self.ur_base[0]
            y_base_pos = self.ur_base[1]
            z_base_pos = self.ur_base[2]
            temp_x = (x_pos + x_end_offset + x_base_pos) ** 2
            temp_y = (y_pos + y_end_offset + y_base_pos) ** 2
            temp_z = (z_pos + z_end_offset + z_base_pos) ** 2
            ur_output = math.sqrt(temp_x + temp_y + temp_z)

            # Lower left base
            x_end_offset = self.ll_base_offset[0]
            y_end_offset = self.ll_base_offset[1]
            z_end_offset = self.ll_base_offset[2]
            x_base_pos = self.ll_base[0]
            y_base_pos = self.ll_base[1]
            z_base_pos = self.ll_base[2]
            temp_x = (x_pos + x_end_offset + x_base_pos) ** 2
            temp_y = (y_pos + y_end_offset + y_base_pos) ** 2
            temp_z = (z_pos + z_end_offset + z_base_pos) ** 2
            ll_output = math.sqrt(temp_x + temp_y + temp_z)

            # Lower right base
            x_end_offset = self.lr_base_offset[0]
            y_end_offset = self.lr_base_offset[1]
            z_end_offset = self.lr_base_offset[2]
            x_base_pos = self.lr_base[0]
            y_base_pos = self.lr_base[1]
            z_base_pos = self.lr_base[2]
            temp_x = (x_pos + x_end_offset + x_base_pos) ** 2
            temp_y = (y_pos + y_end_offset + y_base_pos) ** 2
            temp_z = (z_pos + z_end_offset + z_base_pos) ** 2
            lr_output = math.sqrt(temp_x + temp_y + temp_z)

            #Final output
            print("G1 X%d, Y%d, Z%d, E%d ; ") % (ul_output, ur_output, ll_output, lr_output)