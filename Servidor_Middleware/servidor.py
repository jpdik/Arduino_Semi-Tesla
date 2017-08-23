#coding: utf-8

import serial
import bluetooth
import socket
import udpc
from hashlib import md5
import os
import sys

sys.path.insert(0, os.getcwd()[:os.getcwd().rfind('/')])

import constantes as C

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((C.BD_ADDR, C.BD_PORTA))
print 'Bluetooth Connected'
sock.settimeout(1.0)

s = udpc.socketCUDP(socket.AF_INET)

s.bind((C.IP, C.PORTA))

print 'Socket UDPC Connectado'

dados, dados_cli = s.recv(C.CARACTERES_PACOTE)

s.connect(dados_cli)

while True:
	try:

		if not dados:		
			restart_program()

		sock.send(dados)

		if(dados == 'd'):
			frente = sock.recv(9)

			print frente

			s.send(frente)

		dados, dados_cli = s.recv(C.CARACTERES_PACOTE)
	except bluetooth.btcommon.BluetoothError:
		continue

s.close()
