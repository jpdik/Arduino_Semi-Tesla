$(document).ready(function(){
	// esconde o botão de piloto automático que só será mostrado ao realizar o combo

	// Constantes de definição das teclas de movimentação	
	var KEY_DOWN = 40, 
	KEY_UP  = 38, 
	KEY_LEFT = 37, 
	KEY_RIGHT = 39; 

	// Verificação se alguma tecla está pressionada(correção para eventos de teclado)
	var pressionada = false

	// Verificação de piloto automático ativado
	var automatico = false

	//Variavel para atribuição de timer para coleta de dados dos sensores de proximidade(função que ira obter os dados dos sensores).
	var obterdados

	//Sequencia de combo de teclas que precisa ser acerta para poder mostrar o botão de piloto automático(pode ser modificada por aqui).
	var COMBO = [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]

	//Contador que analisa se a próxima tecla do combo está correta.
	var prox = 0

	//Comparador para saber se mostra ou esconde o botão caso o combo seja realizado.
	var exibir = false

	//Função que analisa e realiza o combo de acordo com as teclas pressionadas pelo usuário
	function combo(tecla){
		if(tecla == COMBO[prox]){
			console.log(COMBO[prox])
			prox++;
		}else
			prox = 0;

		if(prox == COMBO.length){
			if(exibir == false){
				$("#plt").css({display: "block"});
				$('#info').css({ 'margin-top': '-10%' }); 
				exibir = true 
			}
			else{
				$("#plt").css({display: "none"});
				$('#info').css({ 'margin-top': '-9%' }); 
				exibir = false 
			}
			prox = 0;
		}
	}

	//Comando enviado via ajax para resposta do carrinho.
	function comando(tipo){
		$.ajax({
			url: window.location.href+'comando/'+tipo,
				success: function (e) {
				    var resp = JSON.parse(e);
				    $('.command').html(resp['resposta'])
				},
				error: function (e) {
					alert(e)
				},
			type: 'POST',
			cache: false,
			contentType: false,
			processData: false
		});
	}

	//Analise de tecla pressionada dentro do body(corpo da página) para realizar os comandos.
	document.querySelector('body').addEventListener('keydown', function(event) {
 
		var tecla = event.keyCode;
	
		combo(tecla);

		if(automatico == false){
			if(pressionada == false){
				if(tecla == KEY_UP) {
					comando('cima')
				
				} else if(tecla == KEY_DOWN) {
				 	comando('baixo')
				
				} else if(tecla == KEY_LEFT) {
				 	comando('esquerda')
				
				} else if(tecla == KEY_RIGHT) {
					comando('direita')
				
				}
			}
			pressionada = true;
		}
 
	});

	//Analise de tecla solta dentro do body(corpo da página) para parar o veículo.
	document.querySelector('body').addEventListener('keyup', function(event) {

		var tecla = event.keyCode;

		if(automatico == false){
			if(tecla == KEY_UP || tecla == KEY_DOWN || tecla == KEY_LEFT || tecla == KEY_RIGHT){
		 		comando('parar');
				$('.command').html("");
			}
 		}
 		pressionada = false
	});

	//tratamentos de funções de mouse

	//cima
	$('#up').mousedown(function(){
		if(automatico == false)
			comando('cima');	
	});

	$('#up').mouseup(function(){
		if(automatico == false){
			comando('parar');
			$('.command').html("");
		}
	});


	//direita
	$('#dn').mousedown(function(){
		if(automatico == false)
			comando('baixo');
	});

	$('#dn').mouseup(function(){
		if(automatico == false){
			comando('parar');
			$('.command').html("");
		}
	});


	//esquerda
	$('#lft').mousedown(function(){
		if(automatico == false)
			comando('esquerda');
	});

	$('#lft').mouseup(function(){
		if(automatico == false){
			comando('parar');
			$('.command').html("");
		}
	});


	//direita
	$('#rgt').mousedown(function(){
		if(automatico == false)
			comando('direita');		
	});

	$('#rgt').mouseup(function(){
		if(automatico == false){
			comando('parar');
			$('.command').html("");
		}
	});

	//Analise do botao de piloto automático caso seja pressionado.
	$('#info button').click(function(){
	    $.ajax({
			url: window.location.href+'piloto',
				success: function (e) {
				    var resp = JSON.parse(e);
				    if(resp['resposta'] == "Piloto Automatico"){				    
				 		$('.command').html(resp['resposta'])
				 		automatico = true;
				 		$('#info button').css({backgroundColor: "green" });
					}
					else{
						$('.command').html(resp['resposta'])
				 		automatico = false;
				 		$('#info button').css({backgroundColor: "red" });
					}


				},
				error: function (e) {
					alert(e)
				},
			type: 'POST',
			cache: false,
			contentType: false,
			processData: false
		});
	});

	//Realiza a conexão do cliente webservices com o servidor do veículo através de um IP e PORTA.
	$('#conectar').click(function(){
		if($("#ip").val()=="" || $("#porta").val()==""){ 
			alert("Campos Ip ou Porta vazios."); 
		}
		else{
		    $.ajax({
				url: window.location.href+'conectar/'+$('#ip').val()+'/'+$('#porta').val(),
					success: function (e) {
					    var resp = JSON.parse(e);
					    $('.content').html(resp['resposta'])

					    //obter_dados();
					},
					error: function (e) {
						var resp = JSON.parse(e);
						alert(resp['resposta'])
					},
				type: 'POST',
				cache: false,
				contentType: false,
				processData: false
			});
		}
	});

	//Finaliza a conexão do cliente webservices com o servidor do veículo.
	$('#desconectar').click(function(){
	    $.ajax({
			url: window.location.href+'desconectar',
				success: function (e) {
				    var resp = JSON.parse(e);
				    $('.content').html(resp['resposta'])	

				    clearInterval(obterdados);		
				},
				error: function (e) {
				},
			type: 'POST',
			cache: false,
			contentType: false,
			processData: false
		});
	});

	//obtém os dados dos sensores do veículo. Esta função cria um timer no javascript quando a conexão for realizada, e finalizada quando for desconectado.
	function obter_dados(){
		obterdados = setInterval(function(){
	    $.ajax({
			url: window.location.href+'dados',
				success: function (e) {
				    var resp = JSON.parse(e);
				    $('.content').html(resp['dados'])
				},
				error: function (e) {
					
				},
			type: 'POST',
			cache: false,
			contentType: false,
			processData: false
		});
	}, 200);
	}
});
