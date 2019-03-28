from Nodo import Nodo
from Estructuras import Cola
from Estructuras import Pila
import sys
import copy

class Main: 

	def __init__(self, ciudad_inicial, ciudades_por_visitar):
		#Condiciones inicales
		self.ciudades = self.conseguir_ciudades()
		self.ciudades_por_visitar = ciudades_por_visitar.split(" ")
		#Busqueda de la solucion
		ruta = self.conseguir_ruta_amplitud(ciudad_inicial)
		self.imprimir_ruta(ruta)

	def conseguir_ruta_amplitud(self, ciudad_inicial):
		#Condiciones inciales
		lista_soluciones = []
		visitados = []
		cola = Cola()
		costo_de_referencia = 1000000

		#cambiar de string a nodos
		ciudad_actual = self.cadena_nodo(ciudad_inicial)

		######### Busqueda por amplitud (BFS) #########
		# Primera iteracion
		ciudad_actual.establecer_ruta_nodo(ciudad_actual.conseguir_ruta_nodo(),ciudad_actual.conseguir_nombre_ciudad())
		visitados = visitados + self.marcar_visita(ciudad_actual)
		if (self.es_solucion(ciudad_actual) == False): #Si no es solucion
			hijos = ciudad_actual.conseguir_hijos()
			for hijo in hijos:
				nombre_hijo = hijo[0]
				if nombre_hijo not in visitados:
					# Establecemos la ciudad hija como nodo
					nodo_hijo = self.cadena_nodo(nombre_hijo)
					# Establecemos un costo y una ruta
					nodo_hijo.establecer_ruta_nodo(ciudad_actual.conseguir_ruta_nodo(), nodo_hijo.conseguir_nombre_ciudad())
					nodo_hijo.establecer_costo(hijo[1]+ciudad_actual.conseguir_costo())
					# Ingresamos la ciudad hija en la cola
					if nodo_hijo.conseguir_costo() < costo_de_referencia:
						cola.push(nodo_hijo)
		else:
			costo_de_referencia = ciudad_actual.conseguir_costo()
			lista_soluciones.append(copy.deepcopy(ciudad_actual))
			return ciudad_actual.conseguir_ruta_nodo()
		ciudad_actual = cola.pop()
		# Iteraciones
		while (cola.esVacio() == False): # Mientras la cola tenga ciudades por visitar
			if (self.es_solucion(ciudad_actual) == False): #Si no es solucion
				hijos = ciudad_actual.conseguir_hijos()
				for hijo in hijos:
					nombre_hijo = hijo[0]
					if nombre_hijo not in visitados:
						# Establecemos la ciudad hija como nodo
						nodo_hijo = copy.deepcopy(self.cadena_nodo(nombre_hijo))
						# Establecemos un costo y una ruta
						nodo_hijo.establecer_ruta_nodo(ciudad_actual.conseguir_ruta_nodo(), nodo_hijo.conseguir_nombre_ciudad())
						nodo_hijo.establecer_costo(hijo[1]+ciudad_actual.conseguir_costo())
						# Ingresamos la ciudad hija en la cola
						if nodo_hijo.conseguir_costo() < costo_de_referencia:
							cola.push(nodo_hijo)
			else:
				costo_de_referencia = ciudad_actual.conseguir_costo()
				lista_soluciones.append(copy.deepcopy(ciudad_actual))
			visitados = visitados + self.marcar_visita(ciudad_actual)
			ciudad_actual = cola.pop()

		ciudad_solucion = self.conseguir_mejor_solucion(lista_soluciones)
		return ciudad_solucion.conseguir_ruta_nodo()


	def es_solucion(self, ciudad_actual):#ciudad_actual = nodo
		#Implementando el metodo
		ciudades_visitadas = ciudad_actual.conseguir_ruta_nodo();#ciudades que ya fueron visitadas
		bandera = True #bandera que nos indica que si se encontro una ciudad de las que se desean visitar, en la lista de visitados
		#por_visitar = ciudad_actual.ciudades_por_visitar;
		for i in self.ciudades_por_visitar:#ciudades que se desean que se visiten
			bandera = True# inicializamos la bandera
			for j in ciudades_visitadas:
				if j == i:#verificamos si la ciudad que se desea visitar, ya fue visitada
					bandera = False#cambiamos la bandera por false, indicando que una de las ciudades por visitar, ya fue visitada
					break          #entonces rompemos el ciclo, y nos pasamos a la siguiente ciudad que se desea visitar
			if bandera:#verificamos la bandera
				return False #si la bandera no cambio, entonces significa que al menos una de las ciudades que se desean visitar, no ha sido visitada
		return True#devolvemos true cuando las ciudades que se desean visitar, ya fueron visitadas

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
		ciudades= open('servidor/src/estados.txt', 'r').read().split("\n")
		lista_ciudades=[]
		for ciudad in ciudades:
			nombre_ciudad= ciudad.split(":")[0]
			lista_hijos=ciudad.split(":")[1].split(",")
			lista_dos_hijos =[]
			for hijo in lista_hijos:
				lista_aux=hijo.split("-")

				hijo = [lista_aux[1],int(lista_aux[0])]
				lista_dos_hijos.append(hijo)


			lista_ciudades.append(Nodo(nombre_ciudad,lista_dos_hijos))
		return lista_ciudades

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
	#"Oradea:Bucarest Neamt" "Ciudad_inicial:Ciudades_por_visitar"
	# Entrada del usuario
	args = sys.argv[1].split(":")
	ciudad_inicial = args[0]
	ciudades_por_visitar = args[1].split(" ")
	# Instancia del programa
	main = Main(args[0], args[1])

