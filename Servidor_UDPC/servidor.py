#coding: utf-8

import serial
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

#try:
bluetooth=serial.Serial(C.PORT_DEV, 9600)# Inicia o objeto de Comunicação Serial e define a velocidade de comunicação com arduino
bluetooth.flushInput() # Comando para melhorar um pouco o desempenho do bluetooth
#except serial.serialutil.SerialException:
	#print 'Não foi possível estabelecer conexão ou encontrar o dispositivo definido em: '+C.PORT_DEV
	#exit()

s = udpc.socketCUDP(socket.AF_INET)

s.bind((C.IP, C.PORTA))

while True:
	dados, dados_cli = s.recv(C.CARACTERES_PACOTE)

	print dados

	bluetooth.write(str.encode(dados)) #Os dados precisam do encode 'b'
	#input_data=bluetooth.readline() #Le dados enviados pelo arduino pelo serial
	#print(input_data.decode()) # Os dados recebidos precisam de um decode
	#time.sleep(0.1) #Pausa mínima entre envios do bluetooth

	if not dados:		
		restart_program()

	
bluetooth.close() #Finaliza a conexão serial com bluetooh

s.close()
