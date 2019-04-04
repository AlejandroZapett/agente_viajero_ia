import time

def decorador(message):
    def tiempo_ejecucion(funcion):
        def wrapped(*args, **kwargs):

            tiempo_inicio = time.time()

            funcion(message[0],message[1],message[3]) #3 argumentos 

            tiempo_final = time.time()

            print("\nTiempo ejecucion ", tiempo_final-tiempo_inicio)

            return funcion(*args, **kwargs)
        return wrapped
    return tiempo_ejecucion


