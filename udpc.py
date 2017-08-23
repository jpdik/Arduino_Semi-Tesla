#coding: utf-8

import socket
import time
import threading
import struct

class Packet:
    """ Classe pacote UDCP """ 
    TYPE_DATA = 1
    TYPE_SYN = 2
    TYPE_ACK = 4
    TYPE_FIN = 5

    PACKET_STRUCT_LENGHT = 16
    
    def __init__(self, data=""):
        self.checksum = 0
        self.type = None
        self.seqnum = 0           
        self.datalength = None
        self.data = data       
        
    def calc_checksum(self, data):
        return reduce(lambda x,y:x+y, map(ord, data))

    def pack(self, seqnum):
        self.type = self.TYPE_DATA
        self.seqnum = seqnum
        self.datalength = 0 if self.data is None else len(self.data)

        return struct.pack("IIII%ds" % (len(self.data),), self.calc_checksum(self.data), self.type, self.seqnum, self.datalength, self.data)
    
    def unpack(self, data):

        self.checksum, self.type, self.seqnum, self.datalength = struct.unpack("IIII", data[:16])
        if self.datalength > 0:       
            (self.data,) = struct.unpack("%ds" % (self.datalength,), data[16:])     

            if self.checksum != self.calc_checksum(self.data):
                return None   
        return self

    def packACK(self, seqnum):
    	self.type = self.TYPE_ACK
    	self.seqnum = seqnum
    	self.datalength = 0
    	return struct.pack("IIII", self.calc_checksum(str(self.type)), self.type, self.seqnum, self.datalength)

    def packFIN(self, seqnum):
    	self.type = self.TYPE_FIN
    	self.seqnum = seqnum
    	self.datalength = 0
    	return struct.pack("IIII", self.calc_checksum(str(self.TYPE_ACK)), self.type, self.seqnum, self.datalength)

    def confirmACK(self, data):
    	self.unpack(data)
    	return True if self.type == self.TYPE_ACK else False


    def __str__(self):
        return "Pacote " + str(self.__dict__)

class socketCUDP(object):
	#Configurações realizadas normalmente como um socket
	def __init__(self, familiaIP=socket.AF_INET):
		self.ip = ""
		self.porta = 8000

		self.seqnum = 0

		self.packet = ""

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

	def nextSeqNumber(self):
		self.seqnum += 1

	# Função que realiza o recebimento dos dados
	#caso ela nao receba os dados
	def recv(self, bytes):	
		dados, dados_cli = (None, None)

		self.packet = Packet()

		while True:
			try:
				dados, dados_cli = self.sock.recvfrom(bytes+16)

				if self.packet.unpack(dados) != None:
					dados = self.packet.data

					self.sock.sendto(self.packet.packACK(self.packet.seqnum+1), dados_cli)

					if self.packet.type == Packet.TYPE_FIN:
						break
					return (dados, dados_cli)

				else:
					continue

			except socket.timeout:
				continue

		return (None, dados_cli)

	#Função que realiza o envio de informações
	#Fazendo....
	def send(self, bytes):
		if self.ip == "":
			return None

		self.packet = Packet(bytes)

		self.nextSeqNumber()

		while True:
			try:
				self.sock.sendto(self.packet.pack(self.seqnum), (self.ip, self.porta))

				#Aguarda confirmação
				dados, dados_cli = self.sock.recvfrom(16)
				
				if self.packet.confirmACK(dados) is True:
					self.seqnum = self.packet.seqnum
					#confirmou
					break
			except socket.timeout:
				continue

	def finalize(self):
		self.nextSeqNumber()

		tryClose = 0
		while True:
			try:
				self.sock.sendto(self.packet.packFIN(self.seqnum), (self.ip, self.porta))

				#Aguarda confirmação
				dados, dados_cli = self.sock.recvfrom(16)
				
				if self.packet.confirmACK(dados) is True:
					self.seqnum = self.packet.seqnum
					#confirmou
					break
			except socket.timeout:
				if tryClose < 3:
					tryClose += 1
					continue
				else:
					break


	#encerra o socket
	def close(self):
		self.sock.close();
