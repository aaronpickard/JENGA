"""
Aaron Pickard
ajp2235
Spring 2019
block.py
This file defines a block, the basic construction object used in Project JENGA.
This file supports Project JENGA, a final project in the Spring 2019 semester of
MEIE 4810 Introduction to Human Spaceflight at Columbia University.
Each brick is 50x25x25mm
"""


class Block(object):

    def __init__(self):
        self.block_l = 0 #block length
        self.block_w = 0 #block width
        self.block_h = 0 #block height
        self.pt_1_l_offset = 0 #offsets for the two pick-up points in 2 coordinates
        self.pt_1_w_offset = 0
        self.pt_2_l_offset = 0
        self.pt_2_w_offset = 0

    def set_block_length(self, n):
        self.block_l = n

    def set_block_height(self, n):
        self.block_h = n

    def set_block_width(self, n):
        self.block_w = n

    def set_pt1_l_offset(self, n):
        self.pt_1_l_offset = n

    def set_pt1_w_offset(self, n):
        self.pt_1_w_offset = n

    def set_pt2_l_offset(self, n):
        self.pt_2_l_offset = n

    def set_pt2_w_offset(self, n):
        self.pt_2_w_offset = n