$(document).ready(function(){
	$('#plt').hide();

	var KEY_DOWN = 40, 
	KEY_UP  = 38, 
	KEY_LEFT = 37, 
	KEY_RIGHT = 39; 



	var cima,baixo,esquerda,direita

	var automatico = false

	var pressionada = false

	var obterdados

	var COMBO = [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]

	var prox = 0

	var exibir = false

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

	function up(){
		$.ajax({
			url: window.location.href+'cima',
					//Ajax events
				success: function (e) {
				    var resp = JSON.parse(e);
				    $('.command').html(resp['resposta'])
				},
				error: function (e) {
					alert(e)
				},
			// Form data
			type: 'POST',
			//Options to tell jQuery not to process data or worry about content-type.
			cache: false,
			contentType: false,
			processData: false
		});
	}

	function down(){
		$.ajax({
			url: window.location.href+'baixo',
					//Ajax events
				success: function (e) {
				    var resp = JSON.parse(e);
				    $('.command').html(resp['resposta'])
				},
				error: function (e) {
					alert(e)
				},
			// Form data
			type: 'POST',
			//Options to tell jQuery not to process data or worry about content-type.
			cache: false,
			contentType: false,
			processData: false
		});
	}

	function left(){
		$.ajax({
			url: window.location.href+'esquerda',
					//Ajax events
				success: function (e) {
				    var resp = JSON.parse(e);
				    $('.command').html(resp['resposta'])
				},
				error: function (e) {
					alert(e)
				},
			// Form data
			type: 'POST',
			//Options to tell jQuery not to process data or worry about content-type.
			cache: false,
			contentType: false,
			processData: false
		});
	}

	function right(){
		$.ajax({
			url: window.location.href+'direita',
					//Ajax events
				success: function (e) {
				    var resp = JSON.parse(e);
				    $('.command').html(resp['resposta'])
				},
				error: function (e) {
					alert(e)
				},
			// Form data
			type: 'POST',
			//Options to tell jQuery not to process data or worry about content-type.
			cache: false,
			contentType: false,
			processData: false
		});
	}

	function parar(){
		$.ajax({
			url: window.location.href+'parar',
					//Ajax events
				success: function (e) {
				    var resp = JSON.parse(e);
				    $('.command').html(resp['resposta'])
				},
				error: function (e) {
					alert(e)
				},
			// Form data
			type: 'POST',
			//Options to tell jQuery not to process data or worry about content-type.
			cache: false,
			contentType: false,
			processData: false
		});
	}

	document.querySelector('body').addEventListener('keydown', function(event) {
 
		var tecla = event.keyCode;
	
		combo(tecla);

		if(automatico == false){
			if(pressionada == false){
				if(tecla == KEY_UP) {
					up();
				
				} else if(tecla == KEY_DOWN) {
				 	down();
				
				} else if(tecla == KEY_LEFT) {
				 	left();
				
				} else if(tecla == KEY_RIGHT) {
					right();
				
				}
			}
			pressionada = true;
		}
 
	});

	document.querySelector('body').addEventListener('keyup', function(event) {
		if(automatico == false){
	 		parar();
			$('.command').html("");
 		}
 		pressionada = false
	});

	$('#up').mousedown(function(){
		if(automatico == false)
			up();		
	});

	$('#up').mouseup(function(){
		if(automatico == false){
			parar();
			$('.command').html("");
		}
	});

	$('#dn').mousedown(function(){
		if(automatico == false)
			down();
	});

	$('#dn').mouseup(function(){
		if(automatico == false){
			parar();
			$('.command').html("");
		}
	});

	$('#lft').mousedown(function(){
		if(automatico == false)
			left();
	});

	$('#lft').mouseup(function(){
		if(automatico == false){
			parar();
			$('.command').html("");
		}
	});

	$('#rgt').mousedown(function(){
		if(automatico == false)
			right();		
	});

	$('#rgt').mouseup(function(){
		if(automatico == false){
			parar();
			$('.command').html("");
		}
	});

	$('#info button').click(function(){
	    $.ajax({
			url: window.location.href+'piloto',
				//Ajax events
				success: function (e) {
				    var resp = JSON.parse(e);
				    if(resp['resposta'] == "Piloto Automatico"){				    
				 		$('.command').html(resp['resposta'])
				 		automatico = true
				 		$('#info button').css({backgroundColor: "green" });
				 		$('#info button').html("Piloto Automático");
					}
					else{
						$('.command').html(resp['resposta'])
				 		automatico = false
				 		$('#info button').css({backgroundColor: "red" });
				 		$('#info button').html("Manual");
					}


				},
				error: function (e) {
					alert(e)
				},
			// Form data
			type: 'POST',
			//Options to tell jQuery not to process data or worry about content-type.
			cache: false,
			contentType: false,
			processData: false
		});
	});

	$('#conectar').click(function(){
	    $.ajax({
			url: window.location.href+'conectar/'+$('#ip').val()+'/'+$('#porta').val(),
				//Ajax events
				success: function (e) {
				    var resp = JSON.parse(e);
				    $('.content').html(resp['resposta'])

				    obter_dados();
				},
				error: function (e) {
					alert(e)
				},
			// Form data
			type: 'POST',
			//Options to tell jQuery not to process data or worry about content-type.
			cache: false,
			contentType: false,
			processData: false
		});
	});

	$('#desconectar').click(function(){
	    $.ajax({
			url: window.location.href+'desconectar',
				//Ajax events
				success: function (e) {
				    var resp = JSON.parse(e);
				    $('.content').html(resp['resposta'])	

				    clearInterval(obterdados);		
				},
				error: function (e) {
				},
			// Form data
			type: 'POST',
			//Options to tell jQuery not to process data or worry about content-type.
			cache: false,
			contentType: false,
			processData: false
		});
	});

	function obter_dados(){
		obterdados = setInterval(function(){
	    $.ajax({
			url: window.location.href+'dados',
				//Ajax events
				success: function (e) {
				    var resp = JSON.parse(e);
				    $('.content').html(resp['dados'])
				},
				error: function (e) {
					
				},
			// Form data
			type: 'POST',
			//Options to tell jQuery not to process data or worry about content-type.
			cache: false,
			contentType: false,
			processData: false
		});
	}, 5000);
	}
});
