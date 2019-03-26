"""
Aaron Pickard
ajp2235
Spring 2019
path_to_wall.py
This file details a basic path planning algorithm for the construction of a wall.
A basic wall is the proof of concept for Milestone 3 of Project JENGA.
The first objective here, which I am trying to accomplish for Milestone 3,
is to produce an algorithm that will output the right code for a wall given hard coded inputs.
Then, time permitting, I will work on implementing both a better path planning algorithm, and the ability
to take in structures of bricks as a file. If these objectives are not accomplished for Milestone 3,
they will be rolled over into Milestone 4.
This file supports Project JENGA, a final project in the Spring 2019 semester of
MEIE 4810 Introduction to Human Spaceflight at Columbia University.
"""

import gcode

path_gcode = gcode.GCode()

class Basic(object):
    """
    Workspace of 2-4m on each side
    We'll use an origin point in the center (gcode will play nice with negative coordinates)

    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.e = 0

    def set_get_point(self, x, y, z, e):
        path_gcode.goto_x = x
        path_gcode.goto_y = y
        path_gcode.goto_z = z
        path_gcode.goto_e = e
        path_gcode.set_pickup_point()

    def set_put_point(self, x, y, z, e):
        path_gcode.goto_x = x
        path_gcode.goto_y = y
        path_gcode.goto_z = z
        path_gcode.goto_e = e
        path_gcode.set_placement_point()

    def algo(self):
        self.set_get_point()

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
    path_gcode.set_units()

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
        self.p =

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
        while choices is None:
            # TODO pop path_stack
            if path_stack is None:
                break
        return p, choices




