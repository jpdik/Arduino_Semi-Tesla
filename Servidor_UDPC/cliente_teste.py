#coding: utf-8

import socket
import udpc
from sys import argv
from hashlib import md5
from hashlib import sha1
import time
import os
import sys

import serial
import time

sys.path.insert(0, os.getcwd()[:os.getcwd().rfind('/')])

import constantes as C

s = udpc.socketCUDP(socket.AF_INET)

s.connect((C.IP, C.PORTA))

while True:
	comando = raw_input("Comando: "); 

	if comando == 'fim':
		s.finalize()
		break

	s.send(comando)

s.close()