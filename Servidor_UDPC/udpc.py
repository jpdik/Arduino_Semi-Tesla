#coding: utf-8

import socket
import bitarray
import time
import threading

ba = bitarray.bitarray()

class socketCUDP(object):
	#Configurações realizadas normalmente como um socket
	def __init__(self, familiaIP=socket.AF_INET):
		self.ip = ""
		self.porta = 8000

		self.familiaIP = familiaIP
		self.protocolo = socket.SOCK_DGRAM

		self.sock = socket.socket(self.familiaIP, self.protocolo)

		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	#essa função é chamada pelo cliente para realizar a conexao de seu socket
	def connect(self, endereco):
		self.ip, self.porta = endereco

	#essa função é chamada pelo servidor, pois é ele que vai fazer a espera de conexões
	def bind(self, endereco):
		self.ip, self.porta = endereco
		self.sock.bind((self.ip, self.porta))

		#setar o timeout que vai analisar o tempo de morte do recv
		self.sock.settimeout(0.0001)

	# Função que realiza o recebimento dos dados
	#caso ela nao receba os dados
	def recv(self, bytes):	
		dados, dados_cli = (None, None)

		while True:
			try:
				dados, dados_cli = self.sock.recvfrom(bytes + 2)

				head = dados[:2]

				dados = dados[2:]

				if head == self.calc_checksum(dados):
					self.sock.sendto('ack', dados_cli)

					if dados == 'fin':
						break

					return (dados, dados_cli)
				else:
					continue
			except socket.timeout:
				continue

		return (None, dados_cli)

	#Realiza o calculo do checksum
	def calc_checksum(self, s):
	    sum = 0
	    for c in s:
	        sum += ord(c)
	    sum = -(sum % 256)
	    return '%2X' % (sum & 0xFF)

	#Função que realiza o envio de informações
	#Fazendo....
	def send(self, bytes):
		if self.ip == "":
			return None

		head = self.calc_checksum(bytes)

		while True:
			try:
				self.sock.sendto(head + bytes, (self.ip, self.porta))

				#Aguarda confirmação
				dados, dados_cli = self.sock.recvfrom(3)

				#confirmou
				break
			except socket.timeout:
				continue

	# OBS: reestruturar pois estava testando com uma string end, usar o bit FIN agora
	def finalize(self):
		self.send('fin')


	#encerra o socket
	def close(self):
		self.sock.close();
