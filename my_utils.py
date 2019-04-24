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
from mpl_toolkits import mplot3d
import csv
import matplotlib.pyplot as plt
from matplotlib import cm
from numpy import linspace

fig = plt.figure()
ax = plt.axes(projection='3d')

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
    print("MAX Z VALUE = " + str(max_val) + " at POINT = " + str(max_point))


def find_illegal_tether_length(file_name, tether_len):
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
            print("ALL TETHER LENGTHS BETWEEN 0 AND " + str(tether_len) + " IN THE INSTRUCTION SET")

def show_path():
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
