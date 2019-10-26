import sys
import socket
import numpy as np
import lzo

from vispy import app, scene
from vispy.util.filter import gaussian_filter

#--------GLOBAL VARIABLES-------#
port = 8080 #Port a utilitzar pel socket
counter = 1 #Frame counter

#---------AUX FUNCTIONS---------#
#Funcio per fer update del plot
def updatePlot(plot):
    global counter
    receive_frame(counter)
    counter += 1
    #plot.set_data(z=z)

#Funcio per rebre un frame de profunditat de la raspi,
#retorna un array de numpy amb tota la informació Z
def receive_frame(counter):
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

    #Descomprimim el bytearray, sabem que descomprimit ha de
    #ocupar el doble de nombre de posicions del array en bytes
    #global z_positions
    #data = lzo.decompress(data, False, z_positions*2)

    #Generem matriu de profunditat a partir del byetarray
    ##global x_positions, y_positions
    ##Z = np.frombuffer(data, dtype=np.uint16)
    ##Z = Z.reshape(y_positions, x_positions)
    ##return Z

#---------SOCKET SETUP----------#
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

#--------PLOTTING SETUP--------#
canvas = scene.SceneCanvas(keys='interactive', bgcolor='w')
view = canvas.central_widget.add_view()
view.camera = scene.TurntableCamera(up='z', fov=60)

# Simple surface plot example
# x, y values are not specified, so assumed to be 0:50
z = np.random.normal(size=(x_positions, y_positions), scale=200)
p1 = scene.visuals.SurfacePlot(z=z, color=(0.3, 0.3, 1, 1), shading='flat')
p1.transform = scene.transforms.MatrixTransform()
p1.transform.scale([1/160., 1/160., 1/1000.])
p1.transform.translate([-0.25, -0.5, 0])
p1.transform.rotate(180.0, [0,1,0])
p1.transform.rotate(90.0, [0,0,1])

view.add(p1)

xax = scene.Axis(pos=[[-0.5, -0.5], [0.5, -0.5]], tick_direction=(0, -1),
                 font_size=16, axis_color='k', tick_color='k', text_color='k',
                 domain=(0,159), parent=view.scene)
xax.transform = scene.STTransform(translate=(0, 0, -0.2))

yax = scene.Axis(pos=[[-0.5, -0.5], [-0.5, 0.2]], tick_direction=(-1, 0),
                 font_size=16, axis_color='k', tick_color='k', text_color='k',
                 domain=(0,119), parent=view.scene)
yax.transform = scene.STTransform(translate=(0, 0, -0.2))

# Add a 3D axis to keep us oriented
axis = scene.visuals.XYZAxis(parent=view.scene)

if __name__ == '__main__':
    canvas.show()
    if sys.flags.interactive == 0:
        while True:
            updatePlot(p1)
            #app.process_events()