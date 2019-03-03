from Nodo import Nodo
from Estructuras import Cola
import sys

class Main: 

	def __init__(self, ciudad_inicial, ciudades):
		self.ciudades = self.conseguir_ciudades()
		ruta = []
		self.imprimir_ruta(ruta)

	def conseguir_ruta_iterativa(self, ciudad_inicial, ciudad_final):
		#condiciones inciales

		#cambiar de string a nodos
		ciudad_actual = self.cadena_nodo(ciudad_inicial)
		visitados = []
		cola = Cola()

		#Busqueda por amplitud (BFS)
		while (self.es_solucion(ciudad_actual, ciudad_final) == False):
			visitados.append(ciudad_actual.conseguir_nombre_ciudad())
			hijos = ciudad_actual.conseguir_hijos()
			for hijo in hijos:
				if hijo not in visitados:
					hijo = self.cadena_nodo(hijo)
					hijo.establecer_ruta_nodo(ciudad_actual.conseguir_ruta_nodo(), ciudad_actual.conseguir_nombre_ciudad())
					cola.push(hijo)

			ciudad_actual = cola.pop()

		ciudad_actual.establecer_ruta_nodo(ciudad_actual.conseguir_ruta_nodo(), ciudad_actual.conseguir_nombre_ciudad())
		return ciudad_actual.conseguir_ruta_nodo()


	def es_solucion(self, ciudad_actual, ciudad_final):
		if ciudad_actual.conseguir_nombre_ciudad() == ciudad_final:
			return True
		else:
			return False

	def conseguir_ciudades(self): #regresa una lista de nodo, cada nodo es una ciudad
		ciudades = open('estados.txt', 'r').read().split("\n")#leemos y convertimos a lista
		ciudades = [Nodo(ciudad.split(":")[0], ciudad.split(":")[1].split(",")) for ciudad in ciudades]
		return ciudades

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
		ciudades = self.conseguir_ciudades()

		for ciudad in ciudades:
			print(ciudad.conseguir_nombre_ciudad()+" : ")
			print(ciudad.conseguir_hijos())


if __name__ == '__main__':
	args = sys.argv[1].split(" ")
	#"Neamt Oradea"
	ciudad_inicial = "Urziceni"
	main = Main(args[0], args[1])
	#main.pruebas()

