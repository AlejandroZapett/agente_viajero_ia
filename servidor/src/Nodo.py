class Nodo:
	def __init__(self, nombre_ciudad, lista_hijos):
		self.nombre_ciudad = nombre_ciudad
		self.lista_hijos = lista_hijos
		self.ruta_al_nodo = []

	def conseguir_nombre_ciudad(self):
		return self.nombre_ciudad

	def conseguir_hijos(self):
		return self.lista_hijos

	def conseguir_ruta_nodo(self):
		return self.ruta_al_nodo

	def establecer_ruta_nodo(self, ruta, ciudad):
		self.ruta_al_nodo = ruta + [ciudad]