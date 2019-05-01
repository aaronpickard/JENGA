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
        self.block_l = 50  # block length
        self.block_w = 25  # block width
        self.block_h = 25  # block height
        self.pt_1_l_offset = 12.5  # offsets for the two pick-up points in 2 coordinates
        self.pt_1_w_offset = 12.5  # TODO VERIFY THESE
        self.pt_2_l_offset = 37.5
        self.pt_2_w_offset = 12.5

    def set_block_length(self, n):
        """
        :param n: new block length
        :return: none
        """
        self.block_l = n

    def set_block_height(self, n):
        """
        :param n: new block height
        :return: none
        """
        self.block_h = n

    def set_block_width(self, n):
        """
        :param n: new block width
        :return: none
        """
        self.block_w = n

    def set_pt1_l_offset(self, n):
        """
        :param n: new block point 1 length offset
        :return: none
        """
        self.pt_1_l_offset = n

    def set_pt1_w_offset(self, n):
        """
        :param n: new block point 1 width offset
        :return: none
        """
        self.pt_1_w_offset = n

    def set_pt2_l_offset(self, n):
        """
        :param n: new block point 2 length offset
        :return: none
        """
        self.pt_2_l_offset = n

    def set_pt2_w_offset(self, n):
        """
        :param n: new block point 2 width offset
        :return: none
        """
        self.pt_2_w_offset = n
