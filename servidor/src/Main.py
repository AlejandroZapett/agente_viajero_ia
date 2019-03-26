from Nodo import Nodo
from Estructuras import Cola
from Estructuras import Pila
import sys

class Main: 

	def __init__(self, ciudad_inicial, ciudades_por_visitar):
		self.ciudades = self.conseguir_ciudades()
		self.ciudades_por_visitar = ciudades_por_visitar.split(" ")

		ruta = self.conseguir_ruta_amplitud(ciudad_inicial)
		self.imprimir_ruta(ruta)

	def conseguir_ruta_amplitud(self, ciudad_inicial):
		#condiciones inciales
		lista_soluciones = []
		visitados = []
		cola = Cola()
		costo_de_referencia = 1000000

		#cambiar de string a nodos
		ciudad_actual = self.cadena_nodo(ciudad_inicial)

		#Busqueda por amplitud (BFS)
		#modificar es solución
		while (len(self.ciudades_por_visitar) != 0):
			if ciudad_actual.conseguir_nombre_ciudad() in self.ciudades_por_visitar:
				self.ciudades_por_visitar = [x for x in self.ciudades_por_visitar if x != ciudad_actual.conseguir_nombre_ciudad()]
				cola = Cola()	
			visitados = visitados + self.marcar_visita(ciudad_actual)
			cola.filtrar(visitados)
			hijos = ciudad_actual.conseguir_hijos()
			for hijo in hijos:
				if hijo not in visitados:
					hijo = self.cadena_nodo(hijo)
					hijo.establecer_ruta_nodo(ciudad_actual.conseguir_ruta_nodo(), ciudad_actual.conseguir_nombre_ciudad())
					cola.push(hijo)

			#filtrar cola
			ciudad_actual = cola.pop()

		return ciudad_actual.conseguir_ruta_nodo()


	def es_solucion(self, ciudad_actual):#ciudad_actual = nodo
		#Implementando el metodo
		ciudades_visitadas = ciudad_actual.conseguir_ruta_nodo();#ciudades que ya fueron visitadas
		bandera = true #bandera que nos indica que si se encontro una ciudad de las que se desean visitar, en la lista de visitados
		#por_visitar = ciudad_actual.ciudades_por_visitar;
		for i in ciudades_por_visitar:#ciudades que se desean que se visiten
			bandera = true# inicializamos la bandera
			for j in ciudades_visitadas:
				if j == i:#verificamos si la ciudad que se desea visitar, ya fue visitada
					bandera = false#cambiamos la bandera por false, indicando que una de las ciudades por visitar, ya fue visitada
					break          #entonces rompemos el ciclo, y nos pasamos a la siguiente ciudad que se desea visitar
			if bandera:#verificamos la bandera
				return false #si la bandera no cambio, entonces significa que al menos una de las ciudades que se desean visitar, no ha sido visitada
		return true#devolvemos true cuando las ciudades que se desean visitar, ya fueron visitadas

	def conseguir_mejor_solucion(self, lista_soluciones):
		lista_aux = []
		lista_aux = sorted(lista_soluciones, key = lambda x: x.costo_acumulado)
		nodo_solucion = lista_aux[0]	
		return nodo_solucion

	def marcar_visita(self, ciudad):
		if ciudad.establecer_visita() == 1:
			return []
		else:
			return [ciudad.conseguir_nombre_ciudad()]

	def conseguir_ciudades(self): #regresa una lista de nodo, cada nodo es una ciudad
		ciudades = open('servidor/src/estados.txt', 'r').read().split("\n")#leemos y convertimos a lista
		#Implementar método
		#ciudades = [Nodo(ciudad.split(":")[0], ciudad.split(":")[1].split(",")) for ciudad in ciudades]
		#return ciudades

	def cadena_nodo(self, cadena):
		for ciudad in self.ciudades:
			if ciudad.conseguir_nombre_ciudad() == cadena:
				return ciudad

	def imprimir_ruta(self, ruta):
		cadena = ""
		idx = 0
		for ciudad in ruta:
			idx = idx + 1
			cadena = cadena + ciudad + "," if idx < len(ruta) else cadena + ciudad
		print (cadena)

	def pruebas(self):
		print("=== Pruebas Main ===")
		


if __name__ == '__main__':
	args = sys.argv[1].split(":")
	#"Neamt Oradea"
	#"Oradea:Bucarest Neamt"
	ciudad_inicial = args[0]
	ciudades_por_visitar = args[1].split(" ")

	main = Main(args[0], args[1])
	#main.pruebas()

