"""
Aaron Pickard
ajp2235
Spring 2019
main.py
This file contains utility functions that don't really belong anywhere else.
This file supports Project JENGA, a final project in the Spring 2019 semester of
MEIE 4810 Introduction to Human Spaceflight at Columbia University.
"""


def in_to_mm(input):
    output = input/0.039370
    return output


def map_from_arduino(x, in_min, in_max, out_min, out_max):
    """
    Code ported from Arduino, at https://www.arduino.cc/reference/en/language/functions/math/map/
    :param x:
    :param in_min:
    :param in_max:
    :param out_min:
    :param out_max:
    :return:
    """
    temp = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    output = round(temp, 2)
    return output
