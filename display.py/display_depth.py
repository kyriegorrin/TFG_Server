#Imports de I/O
import socket
import sys

#Imports de plotting i data management
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#--------AUX FUNCTIONS ---------#
def z_function(x, y):
    return np.sin(np.sqrt(x ** 2 + y ** 2) * rand.random())

def update_plot(frame_number):
    global plot, X, Y
    plot.remove()
    Z = z_function(X, Y)
    plot = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, 
            cmap='winter', edgecolor='none')
    return plot

#---------SOCKET SETUP----------#
#Port a utilitzar pel socket
port = 8080

#Creacio de socket
try:
    sock = socket.socket()
    print("Socket creat satisfactoriament \n")
except socket.error as err:
    print("Creació de socket fallida:")
    print(err)
    sys.exit()

#Fem bind i posem el socket en mode listen
#No expecifiquem IP pel moment
try:
    sock.bind(('', port))
    sock.listen()
except socket.error as err:
    print("Error de Bind/Listen de socket:")
    print(err)
    sys.exit()

#Bloquejem fins rebre connexió
con, addr = sock.accept()
print("Connexió rebuda, IP")
print(addr)

#Obtenim el nombre de posicions en X i Y del depth map
x_positions = int.from_bytes(con.recv(4), "big")
y_positions = int.from_bytes(con.recv(4), "big")

#--------PLOTTING LOGIC------#

#Activem el plot en mode interactiu i el fem 3D
plt.ion()
fig = plt.figure()
ax = plt.axes(projection="3d")
ax.set_title('Depth Frame')

plot = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, 
            cmap='winter', edgecolor='black')

#Funció d'animació que crida repetidament "update_plot"
animate = animation.FuncAnimation(fig, update_plot, interval=50)

plt.show(block=True)

while counter != 3000:
    #Obtenim tamany del frame a obtenir
    sizeData = con.recv(4)
    byteLength = int.from_bytes(sizeData, "big")

    #Obtenim les dades    
    print("----------------------------------")
    print ("Frame " + str(counter) + " byte length: " + str(byteLength))
    
    data = b''

    while len(data) < byteLength:
        chunk = con.recv(byteLength - len(data))
        print("Chunk size = " + str(len(chunk)))
        if chunk == b'':
            raise RuntimeError("Connexió de socket caiguda")
        data = data + chunk

    print ("Bytes received: " + str(len(data)))
    counter += 1
