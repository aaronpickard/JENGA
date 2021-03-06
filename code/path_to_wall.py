"""
Aaron Pickard
ajp2235
Spring 2019
path_to_wall.py
This file details a basic path planning algorithm for the construction of a wall.
This file supports Project JENGA, a final project in the Spring 2019 semester of
MEIE 4810 Introduction to Human Spaceflight at Columbia University.
"""

import gcode
import block
import os
import my_utils as util

g = gcode.GCode()
brick = block.Block()

class Basic(object):
    """
    Workspace of 2m on each side
    We'll use an origin point in the center (gcode will play nice with negative coordinates)
    """
    def __init__(self):
        self.x = 0  # enables user to "manually" direct motion of the assembly
        self.y = 0
        self.z = 0

    def load_pickup(self, x, y, z):
        """
        :param x: x coordinate of pickup point
        :param y: y coordinate of pickup point
        :param z: z coordinate of pickup point
        :return: none
        """
        g.set_goto_point(x, y, z)
        g.set_pickup_point()

    def load_putdown(self, x, y, z):
        """
        :param x: x coordinate of putdown point
        :param y: y coordinate of putdown point
        :param z: z coordinate of putdown point
        :return: none
        """
        g.set_goto_point(x, y, z)
        g.set_placement_point()

    def load_neutral(self, x, y, z):
        """
        :param x: x coordinate of neutral point
        :param y: y coordinate of neutral point
        :param z: z coordinate of neutral point
        :return: none
        """
        g.set_goto_point(x, y, z)
        g.set_neutral()

    def move_brick(self, pickup, putdown):
        """
        :param pickup: pickup point in [x,y,z] format
        :param putdown: putdown point in  [x,y,z] format
        :return: none
        """
        g.pickup_brick(pickup)
        g.move_vertical(pickup, g.separation_height)
        pickup = [pickup[0], pickup[1], (pickup[2] + g.separation_height)]
        putdown_alias = [putdown[0], putdown[1], (putdown[2] + g.separation_height)]
        g.move_orrian_algo(pickup, putdown_alias)
        g.move_down(putdown_alias, g.separation_height)
        g.putdown_brick(g.current_point)

    def move_back_to_pickup(self):
        """
        :return: none
        """
        pickup = g.pickup_point
        g.move_vertical(g.current_point, g.separation_height)
        pickup = [pickup[0], pickup[1], (pickup[2] + g.separation_height)]
        # self.move_lateral(g.current_point, pickup)
        g.move_orrian_algo(g.current_point, pickup)
        g.move_down(pickup, g.separation_height)

    def move_lateral(self, pickup, putdown):
        """
        :param pickup: pickup point in [x,y,z] format
        :param putdown: putdown point in [x,y,z] format
        :return: none
        """
        g.move_orrian_algo(pickup, putdown)

    def next_brick_in_x_row(self, putdown):
        """
        :param putdown: putdown point in [x,y,z] format to be adjusted
        :return: none
        """
        putdown[0] += brick.block_l
        self.load_putdown(putdown[0], putdown[1], putdown[2])

    def next_brick_in_y_row(self, putdown):
        """
        :param putdown: putdown point in [x,y,z] format to be adjusted
        :return: none
        """
        putdown[1] += brick.block_w
        self.load_putdown(putdown[0], putdown[1], putdown[2])

    def next_horizontal_x_row(self, putdown):
        """
        :param putdown: putdown point in [x,y,z] format to be adjusted
        :return: none
        """
        putdown[1] += brick.block_w
        self.load_putdown(putdown[0], putdown[1], putdown[2])

    def next_horizontal_y_row(self, putdown):
        """
        :param putdown: putdown point in [x,y,z] format to be adjusted
        :return: none
        """
        putdown[0] += brick.block_l
        self.load_putdown(putdown[0], putdown[1], putdown[2])

    def next_vertically_stacked_row(self, putdown, offset_sign):
        """
        :param putdown: putdown point in [x,y,z] format to be adjusted
        :param offset_sign: sign of half-brick-length offset for the next row - valid inputs are '+', '-', or '0'
        :return: none
        """
        if offset_sign == "+":
            putdown[0] = putdown[0] + (brick.block_l/2)
        elif offset_sign == "-":
            putdown[0] = putdown[0] - (brick.block_l / 2)
        elif offset_sign == "0":
            putdown[0] = putdown[0] + 0
        else:
            print("ERROR in next_vertically_stacked_offset_row()")
            g.print_comment("ERROR in next_vertically_stacked_offset_row()")
        putdown[2] += 50
        self.load_putdown(putdown[0], putdown[1], putdown[2])


    def initialize(self):
        """
        :return: none, but sets up environment for algo to execute
        """
        os.remove("output_coordinates.csv")
        os.remove("output_instructions.csv")
        os.remove("output_points.csv")
        os.remove("output_instructions.txt")
        g.separation_height = 100
        g.print_comment("INSTRUCTION SET BEGINS")
        g.print_comment("Instruction set initialization")
        g.set_units()
        g.current_point = [-500, 0, 25]


    def algo2(self):
        """
        :return: none; produces .txt file with G-Code for a notional 12-brick wall and .csv visualization files
        """
        self.initialize()
        pickup = [-500, 0, 25]
        self.load_pickup(pickup[0], pickup[1], pickup[2])
        g.set_feed_rate(20)
        g.set_tether_length()
        putdown = [20, 20, 25]
        original_putdown = [20, 20, 25]
        self.load_putdown(putdown[0], putdown[1], putdown[2])
        g.parabola_operand = 0
        # g.move_orrian_algo(g.neutral_point, pickup)
        # Row 2
        counter = 0
        while counter < 4:
            self.move_brick(pickup, putdown)
            self.move_back_to_pickup()
            self.next_brick_in_x_row(putdown)
            counter += 1
        putdown = [(20+brick.block_l/2), 20, 50]
        self.load_putdown(putdown[0], putdown[1], putdown[2])
        # Row 3
        counter = 0
        while counter < 4:
            self.move_brick(pickup, putdown)
            self.move_back_to_pickup()
            self.next_brick_in_x_row(putdown)
            counter += 1
        """
        temp[2] += brick.block_h
        self.next_vertically_stacked_row(temp, "-")
        """
        putdown = [20, 20, 75]
        self.load_putdown(putdown[0], putdown[1], putdown[2])
        # Row 3
        counter = 0
        while counter < 4:
            self.move_brick(pickup, putdown)
            self.move_back_to_pickup()
            self.next_brick_in_x_row(putdown)
            counter += 1





    def algo(self):
        """
        :return: none; same functionality as algo2() but deprecated
        """
        os.remove("output_coordinates.csv")
        os.remove("output_instructions.csv")
        os.remove("output_points.csv")
        os.remove("output_instructions.txt")


        # g.set_output_file(output_file)
        neutral = g.neutral_point
        pickup = [-800, 0, 0]
        self.load_pickup(pickup[0], pickup[1], pickup[2])
        g.set_feed_rate(20)
        g.set_tether_length()
        putdown = [0, 0, 0]
        self.load_putdown(putdown[0], putdown[1], putdown[2])
        g.move_parabola_xyz(neutral, pickup)

        g.print_comment("Row 1 - 4 bricks")
        i = 0
        while i < 4:
            self.move_brick(pickup, putdown)
            self.move_back_to_pickup()
            self.next_brick_in_x_row(putdown)
            i += 1

        # Adjusts putdown point back to original position
        putdown = [0, 0, 0]
        self.load_putdown(putdown[0], putdown[1], putdown[2])
        self.next_vertically_stacked_row(putdown, "+")

        g.print_comment("Row 2 - 4 bricks offset")
        i = 0
        while i < 4:
            self.move_brick(pickup, putdown)
            self.move_back_to_pickup()
            self.next_brick_in_x_row(putdown)
            i += 1


        """
        g.print_comment("Row 3 - 4 bricks offset back to the original condition")
        putdown = [0, 0, brick.block_h]
        self.load_putdown(putdown[0], putdown[1], putdown[2])
        self.next_vertically_stacked_row(putdown, "-")
        i = 0
        while i < 4:
            self.move_brick(pickup, putdown)
            self.move_back_to_pickup()
            self.next_brick_in_x_row(putdown)
            i += 1
        """

        i = 0
        while i < 4:
            i += 1
            g.move_vertical(putdown, g.separation_height)
        # g.print_comment("move back to neutral")
        # g.move_vertical(pickup, 300)
        # self.load_pickup(pickup[0], pickup[1], (pickup[2]+300))
        # g.move_parabola_xyz(pickup, neutral)
        # print("; INSTRUCTION SET ENDS")
        # print("BEGIN move_horizontal(pickup, neutral)")
        # g.move_horizontal(pickup, neutral)
        # print("END move_horizontal(pickup, neutral)")
        g.print_comment("INSTRUCTION SET ENDS")

        #Verification
        util.find_max_z_value('output_coordinates.csv')
        util.find_illegal_tether_length('output_instructions.csv', 2250)


class Fancy(object):

    """
    Definitinons
    P = {A1, · · · , An} = A sequence of substructures (an assembly path)
    A = A valid substructure
    E = Edges of the graph (struts)
    G = Graph representation of the structure
    M = {σ(A0), · · · , σ(An)} = Instability margins ∀A ∈ P
    S = The set of all substructures
    V = Vertices of the graph (nodes)
    φ = Constructability function
    σ = Stability function
    """

    p = {}
    a = {}
    e = {}
    g = {}
    m = {}
    s = {}
    v = {}
    φ = 0
    σ_limit = 0
    path_stack = {}
    choices = {}

    #Units to mm


    """
    Fancy Algorithm
    Input: The structure to build, G, and the stability limit, σ_limit
    Output: An assembly sequence P of length ≤ |E| + 1 and the instability margins M = {σ(A_0), · · · , σ(A_|P|)} for each step
    1: P = {A_0} = {b}, M = {0}
    2: backtrack =FALSE, path stack =NULL
    3: while P ≤ |E| + 1 do:
    4:   σ_min = ∞, e_next =NULL
    5:   if backtrack =FALSE then:
    6:     choices=every {A_(i+1) ∈ S|φ(A_i, A_(i+1)) = T}
    7:   else:
    8:     P, choices=BackTrack()
    9:     backtrack =FALSE
    10:   end if
    11:   for every A in choices do:
    12:     if σ (A) < σ_min then:
    13:       σ_min = σ (A), e_next = A
    14:     end if
    15:   end for
    16:   if σ_min > σ_limit then:
    17:     backtrack =TRUE
    18:   else:
    19:     remove e_next from choices
    20:     push [P, choices] onto path stack
    21:     P_i = P_(i−1) + e_next, M_i = σ_min
    22:   end if
    23: end while
    24: return P, M
    """


    def algo(self, g, σ_limit):
        """
        :param g: graph representation of the structure
        :param σ_limit: stability limit of structure
        :return: path to assemble structure
        """
        pass

    """
    Backtrack()
    1: while choices =NULL do:
    2:   pop path stack
    3:   if path stack =NULL then:
    4:     terminate
    5:   end if
    6: end while
    7: return P, choices
    """


    def backtrack(self):
        """
        :return: none; deletes bad instructions as helper function to Fancy algo()
        """
        while choices is None:
            # TODO pop path_stack
            if path_stack is None:
                break
        return p, choices




