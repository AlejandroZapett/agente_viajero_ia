class Nodo:
	def __init__(self, nombre_ciudad, lista_hijos):
		self.nombre_ciudad = nombre_ciudad
		self.lista_hijos = lista_hijos
		self.ruta_al_nodo = []
		self.visitas = [0 for x in range(len(lista_hijos)-1)]
		self.sol = False

	def conseguir_nombre_ciudad(self):
		return self.nombre_ciudad

	def conseguir_hijos(self):
		return self.lista_hijos

	def conseguir_ruta_nodo(self):
		return self.ruta_al_nodo

	def establecer_ruta_nodo(self, ruta, ciudad):
		self.ruta_al_nodo = ruta + [ciudad]

	def establecer_visita(self):
		for index, item in enumerate(self.visitas):
			if item == 0:
				self.visitas[index] = 1
				return 1

		return -1

	def conseguir_visitas(self):
		idx = 0
		for x in self.visitas:
			if x == 0:
				idx = idx + 1

		return idx

	def establecer_como_solucion(self):
		self.sol = True
		
	def soy_solucion(self):
		return self.sol
