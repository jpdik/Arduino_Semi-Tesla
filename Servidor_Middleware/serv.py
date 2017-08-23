#coding: utf-8

import serial
import bluetooth
import socket
from hashlib import md5
import os
import sys

sys.path.insert(0, os.getcwd()[:os.getcwd().rfind('/')])

import constantes as C
import udpc

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)

s = udpc.socketCUDP(socket.AF_INET)

s.bind((C.IP, C.PORTA))

print 'Socket UDPC Connectado'

dados, dados_cli = s.recv(1)

s.connect(dados_cli)

while True:
	try:
		if not dados:		
			restart_program()

		print dados

		dados, dados_cli = s.recv(C.CARACTERES_PACOTE)
	except bluetooth.btcommon.BluetoothError:
		continue

s.close()
