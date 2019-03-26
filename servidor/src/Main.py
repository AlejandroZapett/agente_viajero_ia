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


	def es_solucion(self, ciudad_actual):
		#Implemntar método
		pass

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

