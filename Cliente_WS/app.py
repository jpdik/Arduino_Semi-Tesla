# coding: utf-8
import json
import os
import sys
import requests
import udpc
import socket

from flask import Flask, Response, render_template, request

s = udpc.socketCUDP(socket.AF_INET)

piloto_automatico = False

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api():
  name = 'ola'
  if request.method == 'GET':
    return render_template('index.html', name=name) 
  else:
    return json.dumps({'erro': 'Método inválido'})

@app.route('/conectar/<ip>/<porta>', methods=['POST'])
def conectar(ip, porta):
	s.connect((ip, int(porta)))
	return json.dumps({'resposta': 'Conectado'})

@app.route('/desconectar', methods=['POST'])
def desconectar():
	global s

	s.finalize()
	s.close()
	s = udpc.socketCUDP(socket.AF_INET)
	return json.dumps({'resposta': 'Desconectado'})

@app.route('/cima', methods=['POST'])
def cima():
	s.send("F")
	return json.dumps({'resposta': 'Cima'})

@app.route('/baixo', methods=['POST'])
def baixo():
	s.send("T")
	return json.dumps({'resposta': 'Baixo'})

@app.route('/direita', methods=['POST'])
def direita():
	s.send("D")
	return json.dumps({'resposta': 'Direita'})

@app.route('/esquerda', methods=['POST'])
def esquerda():
	s.send("E")
	return json.dumps({'resposta': 'Esquerda'})

@app.route('/parar', methods=['POST'])
def parar():
	s.send("p")
	return json.dumps({'resposta': 'parar'})

@app.route('/dados', methods=['POST'])
def dados():
	return json.dumps({'dados': 'Proximidade: 5.00 cm<br>Proximidade: 5.00 c<br>Proximidade: 5.00 c<br>Proximidade: 5.00 c<br>Proximidade: 5.00 cm<br>Proximidade: 5.00 cm<br>Proximidade: 5.00 cm<br>Proximidade: 5.00 cm<br>Proximidade: 5.00 cm<br>Proximidade: 5.00 cm'})

@app.route('/piloto', methods=['POST'])
def piloto():
	global piloto_automatico

	if piloto_automatico == False:
		s.send("P")
		piloto_automatico = True
		return json.dumps({'resposta': 'Piloto Automatico'})
	else:
		s.send("M")
		piloto_automatico = False
		return json.dumps({'resposta': 'Manual'})


if __name__ == "__main__":
  app.run(debug=True)
