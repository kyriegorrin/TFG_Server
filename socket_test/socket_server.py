import socket
import sys

#Port a utilitzar
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

#Bucle de recepció de dades
#Rebem i printem dades de test
counter = 0

while counter != 100:
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
