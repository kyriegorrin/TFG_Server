#Imports de I/O
import socket
import sys

#Imports de plotting i data management
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random as rand

#--------AUX FUNCTIONS ---------#
def z_function(x, y):
    return np.sin(np.sqrt(x ** 2 + y ** 2) * rand.random())

def update_plot(frame_number):
    global plot, X, Y
    plot.remove()
    Z = receive_frame(frame_number)
    plot = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, 
            cmap='winter', edgecolor='none')
    return plot

#Funcio per rebre un frame de profunditat de la raspi,
#retorna un array de numpy amb tota la informació Z
def receive_frame(counter):
    #Obtenim tamany del frame a obtenir
    sizeData = con.recv(4)
    byteLength = int.from_bytes(sizeData, "big")
    numElems = byteLength // 2

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

    global x_positions, y_positions
    Z = np.frombuffer(data, dtype=np.uint16)
    Z = Z.reshape(y_positions, x_positions)
    return Z

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
z_positions = x_positions * y_positions

print("Especificacions del frame:")
print("X: " + str(x_positions) + " elements")
print("Y: " + str(y_positions) + " elements")
print("Total: " + str(z_positions) + " elements")

#--------PLOTTING LOGIC------#
#Creem els vectors i meshgrids per representar
X = np.arange(x_positions)
Y = np.arange(y_positions)
X,Y = np.meshgrid(X, Y)
Z = np.zeros((y_positions, x_positions))

#Activem el plot en mode interactiu i el fem 3D
plt.ion()

fig = plt.figure()
ax = plt.axes(projection="3d")
ax.set_title('Depth Frame')

plot = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, 
            cmap='winter', edgecolor='black')
        
#Funció d'animació que crida repetidament "update_plot"
animate = animation.FuncAnimation(fig, update_plot, 
                                interval=100)

plt.show(block=True)