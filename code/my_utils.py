"""
Aaron Pickard
ajp2235
Spring 2019
my_utils.py
This file contains utility functions that could go in a variety of locations.
This file supports Project JENGA, a final project in the Spring 2019 semester of
MEIE 4810 Introduction to Human Spaceflight at Columbia University.
"""
import csv
import matplotlib.pyplot as plt
from matplotlib import cm
from numpy import linspace

fig = plt.figure()
ax = plt.axes(projection='3d')

def in_to_mm(input):
    """
    :param input: in inches
    :return: output, which is inches converted to mm
    """
    output = input/0.039370
    return output

def map_from_arduino(x, in_min, in_max, out_min, out_max):
    """
    Code ported from Arduino, at https://www.arduino.cc/reference/en/language/functions/math/map/
    :param x: input value to be converted
    :param in_min:
    :param in_max:
    :param out_min:
    :param out_max:
    :return: the mapping of the input in the output coordinate frame
    """
    temp = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    output = round(temp, 2)
    return output


def find_max_z_value(file_name):
    """
    :param file_name: name of a .csv file containing [x,y,z] data points assumed to be in a cartesian coordinate frame
    :return: print statement identifying the maximum z-value & the point where it happens
             in a local cartesian coordinate frame
    """
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
    print("MAX Z VALUE = " + str(max_val) + " at POINT = " + str(max_point))


def find_illegal_tether_length(file_name, tether_len):
    """
    :param file_name: name of a .csv file with tether lengths
    :param tether_len: length of tether
    :return: print statements identifying points where one tether's length exceeds tether_len, which is a problem,
             because then the tether may detach from the base station
    """
    x = []
    y = []
    z = []
    e = []
    max_len = float(tether_len)
    max_point = [0,0,0]
    illegal = 0
    with open(str(file_name), 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            if (row[0] == "ul_output") or (row[0] == "[-999"):
                pass
            elif float(row[0]) >= max_len:
                illegal_val = float(row[0])
                illegal_point = [row[0], row[1], row[2], row[3]]
                print("ILLEGAL TETHER LENGTH X = " + str(illegal_val) + " at POINT = " + str(illegal_point))
                illegal = 1
            elif float(row[1]) >= max_len:
                illegal_val = float(row[1])
                illegal_point = [row[0], row[1], row[2], row[3]]
                print("ILLEGAL TETHER LENGTH Y = " + str(illegal_val) + " at POINT = " + str(illegal_point))
                illegal = 1
            elif float(row[2]) >= max_len:
                illegal_val = float(row[2])
                illegal_point = [row[0], row[1], row[2], row[3]]
                print("ILLEGAL TETHER LENGTH Z = " + str(illegal_val) + " at POINT = " + str(illegal_point))
                illegal = 1
            elif float(row[3]) >= max_len:
                illegal_val = float(row[3])
                illegal_point = [row[0], row[1], row[2], row[3]]
                print("ILLEGAL TETHER LENGTH A= " + str(illegal_val) + " at POINT = " + str(illegal_point))
                illegal = 1
            else:
                pass
        if illegal == 0:
            print("NO ILLEGAL TETHER LENGTH FOUND")
            print("ALL TETHER LENGTHS IN THE INSTRUCTION SET ARE LESS THAN " + str(tether_len) + "")

def show_path():
    """
    :return: matplotlib  plot of path taken by end effector to place bricks in assembling the structure defined by
             output_coordinates.csv
    """
    x = []
    y = []
    z = []
    with open('output_coordinates.csv','r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            if row[0] != 'x':
                x.append(float(row[0]))
            if row[1] != 'y':
                y.append(float(row[1]))
            if row[2] != 'z':
                z.append(float(row[2]))
    plt.plot(x,y,z, label='Loaded from file!')
    ax.text2D(0.2, 0.95, "End Effector Path for a Notional 12-Brick Wall", transform=ax.transAxes)
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')
    zline = z
    xline = x
    yline = y
    # ax.plot3D(xline, yline, zline, 'grey')
    ax.scatter(xline, yline, zline, zdir='z', s=1, c='blue', depthshade=True)
    plt.show()

def show_path_2():
    """
    :return: none
             FUNCTION NOT FUNCTIONAL, DEVELOPMENT STOPPED
    """
    x = []
    y = []
    z = []
    start = 0.0
    stop = 1.0
    number_of_lines = 1000
    cm_subsection = linspace(start, stop, number_of_lines)

    colors = [cm.jet(x) for x in cm_subsection]

    plt.ylabel('Brick Number')
    plt.show()
    with open('output_coordinates.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            if row[0] != 'x':
                x.append(float(row[0]))
            if row[1] != 'y':
                y.append(float(row[1]))
            if row[2] != 'z':
                z.append(float(row[2]))
    for i, color in enumerate(colors):
        plt.axhline(i, color=color)
    plt.plot(x, y, z, label='Loaded from file!')
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')
    zline = z
    xline = x
    yline = y
    ax.plot3D(xline, yline, zline, cmap='viridis')
    plt.show()


def show_putdown_points():
    """
    :return: matplotlib plot of all the points at which bricks are released, based on 'output_points.csv'
    """
    x = []
    y = []
    z = []
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    with open('output_points.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            if row[0] != 'x':
                x.append(float(row[0]))
            if row[1] != 'y':
                y.append(float(row[1]))
            if row[2] != 'z':
                z.append(float(row[2]))
    ax = plt.axes(projection='3d')
    ax.text2D(0.2, 0.95, "Brick Placement Locations for a Notional 12-Brick Wall", transform=ax.transAxes)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.scatter(x, y, z, c=z, cmap='viridis', linewidth=5)
    plt.show()
