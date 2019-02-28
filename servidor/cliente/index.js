const socket = io();

//DOM Elements
var estado_inicial = "";
var estado_final = "";
var submit_button = document.getElementById('submit-button');

//Submit function
submit_button.addEventListener('click', function(){
	console.log("submiting request");

	estado_inicial = document.getElementById('ei').value;
	estado_final = document.getElementById('ef').value;

	arg = entradas_cadena(estado_inicial, estado_final);

	socket.emit('request', arg);
});

//Socket function
socket.on('response', function(message){
	console.log("Desde python: " + message)
});
//Auxiliar functionsç
function cadena_lista(cadena){}

function entradas_cadena(ei, ef){}