#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import socket


try:
    SERVER = sys.argv[2].split('@')[-1].split(':')[0]  # ip del server
    PORT = int(sys.argv[2].split(':')[-1])
    METOD = sys.argv[1].upper()  # upper me lo pone en mayusculas
    RECEIVER = sys.argv[2].split('@')[0]
    print(SERVER + ' ' + str(PORT) + ' ' + METOD + ' ' + RECEIVER)

except:
    sys.exit('Usage: client.py method receiver@ip:SIPport')

my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

LINE = (METOD + ' sip:' + RECEIVER + '@' + SERVER + ' SIP/2.0')
my_socket.send(bytes(LINE, 'utf-8') + b'\r\n\r\n')
data = my_socket.recv(1024)

received_line = data.decode('utf-8')
confirmation_invite = ('SIP/2.0 100 Trying\r\n\r\n'
                       'SIP/2.0 180 Ring\r\n\r\n'
                       'SIP/2.0 200 OK\r\n\r\n')
if (METOD == 'INVITE') and (received_line == confirmation_invite):
    METOD = 'ACK'
    LINE = (METOD + ' sip:' + RECEIVER + '@' + SERVER + ' SIP/2.0')
    my_socket.send(bytes(LINE, 'utf-8') + b'\r\n\r\n')

print('Recibido -- ', data.decode('utf-8'))
print("Terminando socket...")
my_socket.close()
print("Fin.")
