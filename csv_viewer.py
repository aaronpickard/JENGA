from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import csv
import matplotlib.pyplot as plt
fig = plt.figure()
ax = plt.axes(projection='3d')

def output_coordinates():
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

output_coordinates()