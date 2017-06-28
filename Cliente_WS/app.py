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

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api():
  if request.method == 'GET':
    return render_template('index.html') 
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

@app.route('/comando/<tipo>', methods=['POST'])
def comando(tipo):
	if tipo == 'cima':
		s.send("F")
	elif tipo == 'baixo':
		s.send("T")
	elif tipo == 'direita':
		s.send("D")
	elif tipo == 'esquerda':
		s.send("E")
	elif tipo == 'parar':
		s.send("p")
	else:
		return json.dumps({'resposta': 'desconhecido'})

	return json.dumps({'resposta': tipo})

@app.route('/dados', methods=['POST'])
def dados():
	return json.dumps({'dados': 'Proximidade Frente: 5.00 cm<br>Proximidade atrás: 5.00 cm<br>'})

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
  app.run(host= '192.168.1.102', debug=True)
