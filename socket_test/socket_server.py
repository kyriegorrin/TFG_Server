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
    sock.bind((''), port)
    sock.listen()
except socket.error as err:
    print("Error de Bind/Listen de socket:")
    print(err)
    sys.exit()

#Bloquejem fins rebre connexió
con, addr = s.accept()
print("Connexió rebuda, IP -> " + addr)

#Rebem dades de test
con.recv()