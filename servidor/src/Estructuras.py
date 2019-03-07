class Cola:
	def __init__(self):
		self.lista = []

	def push(self,elemento):
		self.lista.insert(0,elemento)

	def pop(self):
		return self.lista.pop()

	def esVacio(self):
		return len(self.lista) == 0

	def filtrar(self, visitados):
		self.visitados = visitados
		self.lista = list(filter(self.filtro_quitar, self.lista))

	def filtro_quitar(self, visita):
		if visita.conseguir_nombre_ciudad() in self.visitados:
			return False
		else:
			return True

class Pila:
	def  __init__(self):
		self.lista=[]
	def push(self, elemento):
		self.lista.append(elemento)
	def pop(self):
		return self.lista.pop()
	def esVacio(self):
		return len(self.lista)==0

	def filtrar(self, visitados):
		self.visitados = visitados
		self.lista = list(filter(self.filtro_quitar, self.lista))

	def filtro_quitar(self, visita):
		if visita.conseguir_nombre_ciudad() in self.visitados:
			return False
		else:
			return True