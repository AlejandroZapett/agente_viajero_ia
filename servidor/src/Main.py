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
			#print(self.distancia_linea_recta([1,2],[2,2])) ejemplo
			
			#Busqueda de la solucion
			ruta = self.conseguir_ruta(ciudad_inicial, tipo)
			self.imprimir_ruta(ruta)
			#ruta = self.conseguir_ruta_el_mejor(ciudad_inicial)
		
		def conseguir_ruta(self, ciudad_inicial, tipo):
			if (tipo == "voraz"):
				return self.conseguir_ruta_voraz(ciudad_inicial)
			elif (tipo == "a"):
				return self.conseguir_ruta_a_estrella(ciudad_inicial)
			elif (tipo == "amplitud"):
				return self.conseguir_ruta_el_mejor(ciudad_inicial)

		def conseguir_ruta_el_mejor(self, ciudad_inicial):
			#Condiciones inciales
			lista_soluciones = []
			visitados = []
			visitados_aux = []
			cola = Cola()
			costo_de_referencia = 1000000

			#cambiar de string a nodos
			ciudad_actual = self.cadena_nodo(ciudad_inicial)

			######### Busqueda el mejor #########
			# Primera iteracion
			ciudad_actual.establecer_ruta_nodo(ciudad_actual.conseguir_ruta_nodo(),ciudad_actual.conseguir_nombre_ciudad())
			visitados_aux.append(ciudad_actual.conseguir_nombre_ciudad())
			visitados = visitados + self.marcar_visita(ciudad_actual, visitados_aux)
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
				visitados_aux.append(ciudad_actual.conseguir_nombre_ciudad())
				visitados = visitados + self.marcar_visita(ciudad_actual, visitados_aux)
				ciudad_actual = cola.pop()

			ciudad_solucion = self.conseguir_mejor_solucion(lista_soluciones)
			return ciudad_solucion.conseguir_ruta_nodo()
		
		def conseguir_ruta_voraz(self, ciudad_inicial):
			#Condiciones iniciales
			visitados = []
			visitados_aux = []
			lista_espera = []
			ciudad_actual = copy.deepcopy(self.cadena_nodo(ciudad_inicial))
			ciudad_actual.establecer_ruta_nodo(
				ciudad_actual.conseguir_ruta_nodo(),
				ciudad_actual.conseguir_nombre_ciudad()
			)
			######### Busqueda Voraz #########
			while(self.es_solucion(ciudad_actual)==False):
				"""
				print(ciudad_actual.conseguir_nombre_ciudad())
				print(ciudad_actual.conseguir_ruta_nodo())
				print(ciudad_actual.conseguir_costo())
				print(visitados)
				print("\n")"""
				visitados_aux.append(ciudad_actual.conseguir_nombre_ciudad())
				visitados = visitados + self.marcar_visita(ciudad_actual, visitados_aux)
				nombre_ciudad_sol = ""
				for ciudad in self.ciudades_por_visitar:
					nodo_ciudad = copy.deepcopy(self.cadena_nodo(ciudad))
					if (self.distancia_linea_recta(ciudad_actual.get_coordenadas(), nodo_ciudad.get_coordenadas()) == 0):
						nombre_ciudad_sol = ciudad
				self.ciudades_por_visitar = [c for c in self.ciudades_por_visitar if c != nombre_ciudad_sol]
				hijos = ciudad_actual.conseguir_hijos()
				for hijo in hijos:
					nombre_hijo = hijo[0]
					if nombre_hijo not in visitados:
						nodo_hijo = copy.deepcopy(self.cadena_nodo(nombre_hijo))
						nodo_hijo.establecer_ruta_nodo(
							ciudad_actual.conseguir_ruta_nodo(),
							nombre_hijo
						)
						menor_distancia = 100000000
						for ciudad in self.ciudades_por_visitar:
							nodo_ciudad = copy.deepcopy(self.cadena_nodo(ciudad))
							distancia = self.distancia_linea_recta(
								nodo_hijo.get_coordenadas(),
								nodo_ciudad.get_coordenadas()
							) 
							if distancia < menor_distancia:
								menor_distancia = distancia
						nodo_hijo.establecer_costo(menor_distancia)
						lista_espera.append(nodo_hijo)
				lista_espera = self.ordenar_lista(lista_espera)
				ciudad_actual = lista_espera.pop(0)

			return ciudad_actual.conseguir_ruta_nodo()


		def conseguir_ruta_a_estrella(self, ciudad_inicial):
			visitados = []
			lista_espera = []
			ciudad_actual = copy.deepcopy(self.cadena_nodo(ciudad_inicial))
			ciudad_actual.establecer_ruta_nodo(
				ciudad_actual.conseguir_ruta_nodo(),
				ciudad_actual.conseguir_nombre_ciudad()
			)
			while(self.es_solucion(ciudad_actual)==False):
				visitados = visitados + self.marcar_visita(ciudad_actual)
				hijos = ciudad_actual.conseguir_hijos()
				for hijo in hijos:
					nombre_hijo = hijo[0] #nombre
					if nombre_hijo not in visitados:
						nodo_hijo = copy.deepcopy(self.cadena_nodo(nombre_hijo))
						nodo_hijo.establecer_ruta_nodo(
							ciudad_actual.conseguir_ruta_nodo(),
							nombre_hijo
						)
						menor_distancia = 100000000
						for ciudad in self.ciudades_por_visitar:
							nodo_ciudad = copy.deepcopy(self.cadena_nodo(ciudad))
							distancia = self.distancia_linea_recta(
								nodo_hijo.get_coordenadas(),
								nodo_ciudad.get_coordenadas()
							) + hijo[1] #costo
							if distancia < menor_distancia:
								menor_distancia = distancia
						nodo_hijo.establecer_costo(menor_distancia)
						lista_espera.append(nodo_hijo)
				lista_espera = self.ordenar_lista(lista_espera)
				ciudad_actual = lista_espera.pop(0)

			return ciudad_actual.conseguir_ruta_nodo()

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
			print(lista_soluciones)
			lista_aux = sorted(lista_soluciones, key = lambda x: x.costo_acumulado)
			nodo_solucion = lista_aux[0]	
			return nodo_solucion
		####Modifique esta funcion para que devuelva la lista ordenada con respecto a su distancia
		def ordenar_lista(self, lista):
			lista_aux = []
			lista_aux = sorted(lista, key = lambda x: x.conseguir_distancia())#key = lambda x: x.costo_acumulado
			return list(lista_aux)
			
		####Funcion heuristica
		def heuristica_prueba(self, ciudad_inicial)#ciudad final = Bucarest
									#Declaramos la lista de la ciudades con su respectiva distancia en linea recta hacia Bucarest
			lista_hacia_Bucarest = [['Arand',366],['Craviova',160],['Dobreta',242],['Eforie',161],['Fagaras',176],
									['Giurgiu',77],['Hirsova',151],['Iasi',256],['Lugoj',244],['Mehadia',241],
									['Neamt',234],['Oradea',380],['Pitesti',100],['Rimnicu Vilcea',193],['Sibiu',253],
									['Timisoara',329],['Urziceni',80],['Vaslui',199],['Zerind',374]]
			if ciudad_inicial == 'Bucarest':#si la ciudad inicial es la misma que la ciudad final, entonces devolvemos 0
				return 0
			else
				for n in lista_hacia_Bucarest:#Buscamos la ciudad inicial en la lista hacia bucarest
					if ciudad_inicial == n[0]:#Si encuentra la ciudad_inicial en la lista hacia bucarest, entonces devulvemos su respectiva ruta
						return n[1]

		def marcar_visita(self, ciudad, visitados_aux):
			index = 0
			for x in visitados_aux:
				if x == ciudad.conseguir_nombre_ciudad():
					index = index + 1
			if index < ciudad.conseguir_num_visitas():
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

				coordenadas =  [int(x) for x in ciudad.split(":")[2].split("-")]
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

