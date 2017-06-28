# Arduino_Semi-Tesla
Desenvolvimento de um veículo semi-autônomo em Arduino que realiza comunicação Bluetooh com o servidor, e realiza uma ponte de conexão(através de um servidor)que possui um protocolo UDP que implementa confiabilidade e que se comunica com um cliente WebService em Flask:

<p align="center">
  <img src="https://mail.google.com/mail/u/0/?ui=2&ik=1014e4bdc0&view=fimg&th=15c4fe112374eb69&attid=0.1&disp=emb&realattid=ii_15c4fdd151f860ae&attbid=ANGjdJ9jQK79KNneE8n5TTftBs0_IYTEFEwYfmNNDYQtBAUVfVsrrev-dlbjxEmET-HTyT4_eXq63Dh7_8zy4CEjV3jzHq1775chnZlTb0z2Xr18zOnD2vrD0MP2fvA&sz=w936-h666&ats=1498620446855&rm=15c4fe112374eb69&zw&atsh=1"/>
</p>

O protótipo em Arduíno foi construído usando os seguintes materiais:
<pre>
1 Placa Arduino Mega 2560
1 Módulo bluetooth hc-06 (Com divisor de tensão [3.3V])
1 Shield Ponte H L293D
4 Motores
1 Kit chassi com 4 rodas
2 Sensores ultrasonico HCSR04 (frente e trás do veículo)
Jumpers
Resistores
</pre>

Foi programado para que os motores respondesem através de simples comandos enviados via Bluetooth
<pre>
Serial3.read(); //Lê um caractere pela porta Serial 3 (Somente arduino MEGA)
</pre>
São lidos caracteres via Serial Bluetooh, afim de se manter a alta velocidade de troca de informações.

O Servidor recebe a informação do cliente WebService atráves de um Socket com Protocolo UDP Confiável construido em uma classe.
<pre>
dados, dados_cli = s.recv(C.CARACTERES_PACOTE)
</pre>
E os envia para o Arduino pelo Serial.
<pre>
bluetooth.write(str.encode(dados)) #Os dados precisam do encode 'b'
</pre>

Os dados sao recebidos via comandos dados pelo cliente no WebService através da conexão do socket UDP Confiável.
<pre>
@app.route('/comando/<tipo>', methods=['POST'])
def comando(tipo):
	if tipo == 'cima':
		s.send("F") //F representando Frente.
    ...
</pre>

O cliente tem uma ótima interação pela interface, onde ele configura sua comunicação com o servidor.
<p align="center">
  <img src="https://github.com/jpdik/Arduino_Semi-Tesla/blob/master/img/Example_WS.png?raw=true"/>
</p>
