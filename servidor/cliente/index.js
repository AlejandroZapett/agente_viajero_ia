const socket = io();

//DOM Elements
var estado_inicial = "";
var estado_final = "";
var submit_button = document.getElementById('submit-button');
var response_area = document.getElementById('response-area')

//Submit function
submit_button.addEventListener('click', function(){
	console.log("submiting request");

	ciudad_inicial = document.getElementById('ei').value;
	ciudades_por_visitar = document.getElementById('ef').value;

	arg = entradas_cadena(ciudad_inicial, ciudades_por_visitar);

	socket.emit('request', arg);
});

//Socket function
socket.on('response', function(message){
	console.log("Desde python: " + message);
	var ciudades = cadena_lista(message);

	imprimir_ruta(ciudades);
});

//Auxiliar functions
function cadena_lista(cadena){
	var ciudades = cadena.split(",");
	return ciudades;
}

function entradas_cadena(ci, cpv){
	var message = String(ci)+":"+String(cpv);
	console.log(message);
	return message;
}

function imprimir_ruta(ciudades){
	var wrapper = document.createElement("DIV");
	var par = document.createElement("P");
	var text = "Las ruta es ";
	ciudades.forEach(item => {
		text = text + " => " + String(item);
	});
	par.innerHTML = text;
	wrapper.appendChild(par);
	response_area.appendChild(wrapper);
}