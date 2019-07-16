#Imports de I/O
import socket
import sys

#Imports de plotting i data management
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random as rand

X = np.arange(160)
Y = np.arange(120)
X,Y = np.meshgrid(X, Y)
Z = np.zeros((120, 160))

#Activem el plot en mode interactiu i el fem 3D
plt.ion()

fig = plt.figure()
ax = plt.axes(projection="3d")
ax.set_title('Depth Frame')

plot = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, 
            cmap='winter', edgecolor='black')

print(type(plot))

plt.show(block=True)