#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os


class EchoHandler(socketserver.DatagramRequestHandler):

    def handle(self):
        valid_metod = False
        valid_request = False
        line_str = self.rfile.read().decode('utf-8')
        list_linecontent = line_str.split()
        server_metods = ['INVITE', 'ACK', 'BYE']
        metod = list_linecontent[0]
        print('peticion recibida: ', line_str)
        if metod in server_metods:
            valid_metod = True
        else:
            self.wfile.write(b'SIP/2.0 405 Method Not Allowed\r\n\r\n')

        if len(list_linecontent) == 3:  # checkea q la peticion es correcta
            valid_request = True
        else:
            self.wfile.write(b'SIP/2.0 400 Bad Request\r\n\r\n')

        if valid_metod and valid_request:
            if metod == 'INVITE':
                self.wfile.write(bytes('SIP/2.0 100 Trying\r\n\r\n'
                                       'SIP/2.0 180 Ring\r\n\r\n'
                                       'SIP/2.0 200 OK\r\n\r\n', 'utf-8'))
            elif metod == 'ACK':
                os.system('./mp32rtp -i 127.0.0.1 -p 23032 < ' +
                          fichero_audio)
            elif metod == 'BYE':
                self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')

if __name__ == "__main__":
    try:
        serv = socketserver.UDPServer((sys.argv[1], int(sys.argv[2])),
                                      EchoHandler)
        fichero_audio = sys.argv[3]
        if not os.path.isfile(fichero_audio):
            sys.exit('File Error: ' + fichero_audio + ' does not exist')
        print("Listening...")
    except IndexError:
        sys.exit('Usage: server.py IP port audio_file')

    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print('Finalizado servidor')
