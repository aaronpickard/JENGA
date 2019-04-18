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
import csv
import matplotlib.pyplot as plt
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
    with open(str(file_name), 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            if (row[0] == "ul_output") or (row[0] == "[-999"):
                pass
            elif float(row[0]) >= max_len:
                illegal_val = float(row[0])
                illegal_point = [row[0], row[1], row[2], row[3]]
                print("ILLEGAL VALUE X = " + str(illegal_val) + " at POINT = " + str(illegal_point))
            elif float(row[1]) >= max_len:
                illegal_val = float(row[1])
                illegal_point = [row[0], row[1], row[2], row[3]]
                print("ILLEGAL VALUE Y = " + str(illegal_val) + " at POINT = " + str(illegal_point))
            elif float(row[2]) >= max_len:
                illegal_val = float(row[2])
                illegal_point = [row[0], row[1], row[2], row[3]]
                print("ILLEGAL VALUE Z = " + str(illegal_val) + " at POINT = " + str(illegal_point))
            elif float(row[3]) >= max_len:
                illegal_val = float(row[3])
                illegal_point = [row[0], row[1], row[2], row[3]]
                print("ILLEGAL VALUE E= " + str(illegal_val) + " at POINT = " + str(illegal_point))

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
    zline = z
    xline = x
    yline = y
    ax.plot3D(xline, yline, zline, 'gray')
    plt.show()

def show_putdown_points():
    x = []
    y = []
    z = []
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
    ax.scatter(x, y, z, c=z, cmap='viridis', linewidth=0.5)
    plt.show()
