from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import random as rand

def z_function(x, y):
    return np.sin(np.sqrt(x ** 2 + y ** 2) * rand.random())

def update_plot(frame_number, plot):
    plot.remove()
    Z = z_function(X, Y)
    plot = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, 
            cmap='winter', edgecolor='none')
    return plot

#Fem el plot interactiu
plt.ion()

x = np.linspace(-6, 6, 30)
y = np.linspace(-6, 6, 30)

X, Y = np.meshgrid(x, y)
Z = z_function(X, Y)


fig = plt.figure()
ax = plt.axes(projection="3d")
ax.set_title('surface_test')
    
plot = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, 
            cmap='winter', edgecolor='none')

animate = animation.FuncAnimation(fig, update_plot, fargs=(plot), interval=50)

plt.show()