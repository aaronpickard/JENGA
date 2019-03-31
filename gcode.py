"""
Aaron Pickard
ajp2235
Spring 2019
gcode.py
This file defines gcode operations used to assemble blocks into a structure in Project JENGA.
This file supports Project JENGA, a final project in the Spring 2019 semester of
MEIE 4810 Introduction to Human Spaceflight at Columbia University.
"""
from __future__ import division
import math
import numpy as np


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
        self.neutral_point = [1, 1, 500] # x,y,z
        self.pickup_point = [1, 1, 1]
        self.placement_point = [1, 1, 1]
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
        self.parabola_coefficient = 1.5
        self.separation_height = 75  #3x brick height, or brick + pyramid + 25mm height
        self.output_file = "output.txt"
        f = open(self.output_file, "w")
        f.write("; Project JENGA Instruction set")
        f.close()

    # def set_output_file(self, f):
        # self.output_file = f

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
        if self.output_file is not None:
            file = open(self.output_file, "a")
            file.write("G1 F" + str(self.feed_rate) + " ; \n")
            file.close()


    def set_units(self):
        print("G21 ; This program requires operations with the gcode millemeter setting")
        if self.output_file is not None:
            file = open(self.output_file, "a")
            file.write("G21 ; This program requires operations with the gcode millemeter setting \n")
            file.close()

    def set_separation_height(self, h):
        self.separation_height = h

    def set_step_size(self, s):
        self.step_size = s

    def pickup_brick(self, place):
        """
        :param place: This parameter indicates the place at which the brick will be placed.
                      The placement assembly should be here already when the function is called.
        :return: Nothing
        """
        place_x = place[0]
        place_y = place[1]
        place_z = place[2]
        pickup = 999
        self.print_command([pickup, place_y, place_z])

    def putdown_brick(self, place):
        """
        :param place: This parameter indicates the place at which the brick will be placed.
                      The placement assembly should be here already when the function is called.
        :return: Nothing
        """
        place_x = place[0]
        place_y = place[1]
        place_z = place[2]
        putdown = -999
        self.print_command([putdown, place_y, place_z])

    def move_brick_to_placement(self, start, stop):
        # This function picks up a brick at the start point, moves it to the stop point, puts it down, and returns to
        # the start point.
        """
        Development notes
        LINEAR INTERPOLATION gcode ALGORITHM (getting to place and from it)
        1 calculate total distance
            a) start at pickup point (likely to be close to z=0
            b) terminal approach to placement is at least 20mm from both pickup and putdown (that terminate at same
               height?) - discretize in segments of 5 mm??
            c) third point is midpoint of them + function of the linear distance between them up (if  closer dont go as far up)
            d) find inverse parabola using maths
        2 set variable for max distance between points
        3 int divide(ceiling) total distance by max distance to get step distance
        4 I have to discretize the parabola!!!
        5 last step is conversion to tether lengths
        """

        # Variable declaration
        start_x = start[0]
        start_y = start[1]
        start_z = start[2]
        stop_x = stop[0]
        stop_y = stop[1]
        stop_z = stop[2]
        parabola_stop_z = stop[2] + self.separation_height
        parabola_stop = [stop_x, stop_y, parabola_stop_z]

        # The brick has been picked up by calling pickup_brick(place). Assembly is still at the pickup point.
        self.move_vertical(start, self.separation_height)
        start[2] += self.separation_height
        start_z = start[2]
        stop_z += self.separation_height
        self.move_parabola_xz([start_x, start_y, start_z], [stop_x, start_y, stop_z])
        self.move_parabola_yz([stop_x, start_y, stop_z], [stop_x, stop_y, stop_z])  # x & z coord.s set by last call
        self.move_vertical([stop_x, stop_y, stop_z], (-1*self.separation_height))
        # Now put the brick down by calling putdown_brick(place)
        # Return to starting position by invoking this method but swapping the start and stop points

    def move_parabola_xz(self, start, stop):
        # Moves via parabolic arc in the xz frame
        start_x = start[0]
        start_z = start[2]
        stop_x = stop[0]
        stop_z = stop[2]
        midpoint_x = (start_x + stop_x) / 2
        midpoint_z = self.parabola_coefficient * midpoint_x
        self.make_parabola(start_x, start_z, stop_x, stop_z, midpoint_x, midpoint_z, "y", start[1])
        # TODO this is always called first - could it be more efficient to not necessarily go down on to the
        #  placement point since I'll only be on top of it in one direction?
        #  What happens if I put the 3rd parabola point such that the start and stop points are on the same side as
        #  the high point of the parabola? Does this affect path efficiency (defined by # of instructions printed)?
        #  Does this limit the kinds of structures I can build?

    def move_parabola_yz(self, start, stop):
        # Moves via parabolic arc in the yz frame
        start_y = start[1]
        start_z = start[2]
        stop_y = stop[1]
        stop_z = stop[2]
        mid_point_y = (start_y + stop_y) / 2
        midpoint_z = self.parabola_coefficient * mid_point_y
        self.make_parabola(start_y, stop_z, stop_y, stop_z, mid_point_y, midpoint_z, "x", start[0])
        # TODO this is always called second & has a clearance parameter to make sure it doesnt hit another brick
        #  so why shouldn't I do this step in the xy plane, without any of this parabola math?
        #  Would removing vertical motion meaningfully increase the step size (and so decrease the number of steps
        #  required for the move) by allowing more distance to be gained in horizontal motion?

    def move_parabola_xyz(self, start, stop):
        # NOT OPERATIONAL
        # Moves via parabolic arc FIRST in the xz frame and THEN in the yz frame,
        # combining the two move_parabola_wz() functions
        start_x = start[0]
        start_y = start[1]
        start_z = start[2]
        stop_x = stop[0]
        stop_y = stop[1]
        stop_z = stop[2]
        midpoint_x = (start_x + stop_x) / 2
        mid_point_y = (start_y + stop_y) / 2
        midpoint_z = self.parabola_coefficient * midpoint_x
        self.make_parabola(start_x, start_z, stop_x, stop_z, midpoint_x, midpoint_z, "y", start[1])
        midpoint_z = self.parabola_coefficient * mid_point_y
        self.make_parabola(start_y, stop_z, stop_y, stop_z, mid_point_y, midpoint_z, "x", start[0])

    def make_parabola(self, x1, y1, x2, y2, x3, y3, static_var, static_val):
        """
        This particular function was not solely written by a member of the Project JENGA team.
        The code in this function was adapted with modification from the GitHub site of Chris Williams
        http://chris35wills.github.io/parabola_python/

        NOTE Unlike move_vertical(), in which there is no horizontal motion, the step size calculation here is
        based on the division of the non-z coordinate distance traveled into steps based on the maximum step size.
        :param x1: defines x or y coordinate of point 1
        :param y1: defines z coordinate of point 1
        :param x2: defines x or y coordinate of point 2
        :param y2: defines z coordinate of point 2
        :param x3: defines x or y coordinate of point 3
        :param y3: defines z coordinate of point 3
        :param static_var: indicates which value, x or y, is unchanged by this particular function call
        :param static_val: indicates the value of the variable unchanged by this function call
        """
        denom = 1.0 * (x1 - x2) * (x1 - x3) * (x2 - x3)
        if denom == 0:
            denom = 0.000000000000001
            # TODO this feels hacky - is it ok?
        a = (x3 * (y2 - y1) + x2 * (y1 - y3) + x1 * (y3 - y2)) / denom
        b = (x3 * x3 * (y1 - y2) + x2 * x2 * (y3 - y1) + x1 * x1 * (y2 - y3)) / denom
        c = (x2 * x3 * (x2 - x3) * y1 + x3 * x1 * (x3 - x1) * y2 + x1 * x2 * (x1 - x2) * y3) / denom
        x_pos = np.arange(x1, x2, self.step_size)  # x is the nonstatic var so this should be the range
        """
        DELETE THIS after verifying code works
        if static_var == "x":  # creating a yz graph
            # x_pos = np.arange(self.ll_base[0], self.lr_base[0], self.step_size)
            # confusingly, x_pos refers to the y dimension in the line of code above
        elif static_var == "y":  # creating an xz graph
            x_pos = np.arange(self.ll_base[1], self.ul_base[1], self.step_size)
        """
        z_pos = []  # stored so if we wanted to do something with the coordinate pairs we could
        # Calculate y values
        for x in range(len(x_pos)):
            x_val = x_pos[x]
            z = (a * (x_val ** 2)) + (b * x_val) + c
            z_pos.append(z)
            if static_var == "x":
                self.print_command([static_val, x_val, z])  # If x is static it never changes
            elif static_var == "y":
                self.print_command([x_val, static_val, z])  # If y is static it never changes
            else:
                print("; make_parabola() can only create parabolas in the xz and yz planes. \n")
                if self.output_file is not None:
                    file = open(self.output_file, "a")
                    file.write("; make_parabola() can only create parabolas in the xz and yz planes. \n")
                    file.close()
                break

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
            # calculate new intermediate position
            intermediate[2] = intermediate[2] + self.step_size
            # convert to change in height & print instruction
            self.print_command(intermediate)
            if stop_z - intermediate[2] < self.step_size:
                # calculate new intermediate position
                intermediate[2] = intermediate[2] + (stop_z - intermediate[2])
                # convert to change in height & print instruction
                self.print_command(intermediate)
                break

    def move_horizontal(self, start, stop):
        # This method works by stepping between coplanar start and stop points linearly.
        # Usage is recommended only for points in the same z-plane (height).
        """
        1 get current location (x,y,z)
        2 get intermediate end effector positions (x,y,z,p) - p is boolean
        3 iterate through each intermediate position and from that convert to tether length
        """
        start_x = start[0]
        start_y = start[1]
        start_z = start[2]
        stop_x = stop[0]
        stop_y = stop[1]
        stop_z = stop[2]
        intermediate = [start_x, start_y, start_z]
        # get unit vector
        vector_x = start_x + stop_x
        vector_y = start_y + stop_y
        vector_z = start_z + stop_z
        vector_mag = math.sqrt(vector_x**2 + vector_y**2 + vector_z**2)
        unit_x = vector_x/vector_mag*self.step_size
        unit_y = vector_y/vector_mag*self.step_size
        unit_z = vector_z/vector_mag*self.step_size
        unit = [unit_x, unit_y, unit_z]  # now I have a unit vector w/ length step_size

        while (start_x != stop_x) or (start_y != stop_y) or (start_z != stop_z):
            # calculate new intermediate position
            if intermediate[0] != stop_x:
                intermediate[0] += unit[0]
                if intermediate[0] - stop_x < self.step_size:  # handles case where value is approaching stop value
                    intermediate[0] = stop_x
            if intermediate[1] != stop_y:
                intermediate[1] += unit[1]
                if intermediate[1] - stop_y < self.step_size:
                    intermediate[1] = stop_y
            if intermediate[2] != stop_z:
                intermediate[2] += unit[2]
                if intermediate[2] - stop_z < self.step_size:
                    intermediate[2] = stop_z
            intermediate = [intermediate[0], intermediate[1], intermediate[2]]
            self.print_command(intermediate)
            # convert to change in height & print instruction
            # TODO how do I limit this in the case where the unit vector's size doesnt evenly divide the distance
            #  between the start and stop points? That's what I'm missing for this to really be functional
            # TODO how do I keep this function from running away in an infinite loop?

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
            if self.output_file is not None:
                file = open(self.output_file, "a")
                file.write("M8 ; pickup \n")
                file.close()

        elif x_pos == -999:
            # Putdown
            print("M9 ; ")
            if self.output_file is not None:
                file = open(self.output_file, "a")
                file.write("M9 ; putdown \n")
                file.close()

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

            # Print this statement
            # print("G1 X%d, Y%d, Z%d, E%d ; \n") % (ul_output, ur_output, ll_output, lr_output)
            print("G1 X"+str(ul_output)+", Y"+str(ur_output)+", Z"+str(ll_output)+", E"+str(lr_output)+" ;")
            if self.output_file is not None:
                file = open(self.output_file, "a")
                file.write("G1 X"+str(ul_output)+", Y"+str(ur_output)+", Z"+str(ll_output)+", E"+str(lr_output)+" ; \n")
                file.close()
            # TODO Enable users to make comments on commands in the path_to_wall function
