from Nodo import Nodo
from Estructuras import Cola
from Estructuras import Pila
from Tiempo import tiempo_ejecucion
from math import sqrt
import sys
import copy
import argparse

def agente_viajero(argumentos):
    	
	@tiempo_ejecucion(argumentos)
	class Main: 

		def __init__(self, ciudad_inicial, ciudades_por_visitar, tipo):
			#Condiciones inicales
			self.ciudades = self.conseguir_ciudades()
			self.ciudades_por_visitar = ciudades_por_visitar
			self.tipo_busqueda = tipo
			print("===============")
			print(ciudad_inicial)
			print(self.ciudades_por_visitar)
			print(self.tipo_busqueda)
			print("===============")
			#print(self.distancia_linea_recta([1,2],[2,2])) ejemplo
			#Busqueda de la solucion
			#ruta = self.conseguir_ruta_el_mejor(ciudad_inicial)
			#self.imprimir_ruta(ruta)

		def conseguir_ruta_el_mejor(self, ciudad_inicial):
			#Condiciones inciales
			lista_soluciones = []
			visitados = []
			cola = Cola()
			costo_de_referencia = 1000000

			#cambiar de string a nodos
			ciudad_actual = self.cadena_nodo(ciudad_inicial)

			######### Busqueda el mejor #########
			# Primera iteracion
			ciudad_actual.establecer_ruta_nodo(ciudad_actual.conseguir_ruta_nodo(),ciudad_actual.conseguir_nombre_ciudad())
			visitados = visitados + self.marcar_visita(ciudad_actual)
			if (self.es_solucion(ciudad_actual) == False): #Si no es solucion
				hijos = ciudad_actual.conseguir_hijos()
				for hijo in hijos:
					nombre_hijo = hijo[0]
					if nombre_hijo not in visitados:
						# Establecemos la ciudad hija como nodo
						nodo_hijo = copy.deepcopy(self.cadena_nodo(nombre_hijo))
						# Establecemos un costo y una ruta
						nodo_hijo.establecer_ruta_nodo(ciudad_actual.conseguir_ruta_nodo(), nodo_hijo.conseguir_nombre_ciudad())
						nodo_hijo.establecer_costo(hijo[1])
						# Ingresamos la ciudad hija en la cola
						if nodo_hijo.conseguir_costo() < costo_de_referencia:
							cola.push(nodo_hijo)
			else:
				costo_de_referencia = ciudad_actual.conseguir_costo()
				lista_soluciones.append(copy.deepcopy(ciudad_actual))
				#return ciudad_actual.conseguir_ruta_nodo()
		
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
					#return ciudad_actual.conseguir_ruta_nodo()
				visitados = visitados + self.marcar_visita(ciudad_actual)
				ciudad_actual = cola.pop()

			ciudad_solucion = self.conseguir_mejor_solucion(lista_soluciones)
			return ciudad_solucion.conseguir_ruta_nodo()
		
		def conseguir_ruta_voraz(self):
			pass

		def conseguir_ruta_a_estrella(self):
			pass

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
			ciudades= open('servidor/src/Estados.txt', 'r').read().split("\n")
			lista_ciudades=[]
			for ciudad in ciudades:
				nombre_ciudad= ciudad.split(":")[0]
				lista_hijos=ciudad.split(":")[1].split(",")
				lista_dos_hijos =[]
				for hijo in lista_hijos:
					lista_aux=hijo.split("-")

					hijo = [lista_aux[1],int(lista_aux[0])]
					lista_dos_hijos.append(hijo)
				coordenadas = []
				for x in ciudad.split(":")[2].split("-"):
				 coordenadas.append(int(x))

				lista_ciudades.append(Nodo(nombre_ciudad,lista_dos_hijos,coordenadas))
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
		
		def distancia_linea_recta(self,x,y):
			costo = 27 #cambiar si es necesario
			a = abs(x[0] - y[0]) * costo
			b = abs(x[1] - y[1]) * costo
			return  sqrt(pow(a,2) + pow(b,2))


		
	main = Main()

def leer_argumentos():
	parser = argparse.ArgumentParser(description='Definir tipo de busqueda y conjunto de ciudades')
	parser.add_argument('-t','--tipo_busqueda', required=True,help= 'Tipo de busqueda: voraz, amplitud o a')
	parser.add_argument('-a','--ciudades',required=True,help='Ciudad inicial y ciudades a visitar')
	args = parser.parse_args()
	argumentos=[
		args.ciudades.split(":")[0], 
		args.ciudades.split(":")[1].split(","),
		args.tipo_busqueda
	]

	return argumentos		


if __name__ == '__main__':
	#"Oradea:Bucarest,Neamt" "Ciudad_inicial:Ciudades_por_visitar"
	# Entrada del usuario
	argumentos = leer_argumentos()
	# Instancia del programa
	agente_viajero(argumentos)

