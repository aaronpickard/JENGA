"""
Aaron Pickard
ajp2235
Spring 2019
main.py
This file contains utility functions that don't really belong anywhere else.
This file supports Project JENGA, a final project in the Spring 2019 semester of
MEIE 4810 Introduction to Human Spaceflight at Columbia University.
"""
import csv

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


def find_max_z_value(file_name):
    x = []
    y = []
    z = []
    max_val = 0
    max_point = [0,0,0]
    with open(str(file_name), 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            if row[0] == "x":
                pass
            elif float(row[2]) > float(max_val):
                max_val = float(row[2])
                max_point = [row[0], row[1], row[2]]
    print("MAX VALUE = " + str(max_val) + " at POINT = " + str(max_point))
