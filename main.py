# Un objeto con un volumen (int) y un valor (int)
class Objeto:

    def __init__(self, volumen: int, valor: int) -> None:
        self.volumen = volumen
        self.valor = valor

    def __repr__(self) -> str:
        return f"\nVolumen: {self.volumen} - Valor: {self.valor}"


# Datos de los objetos dados por el enunciado
objetos: list = [
    Objeto(150, 20),
    Objeto(325, 40),
    Objeto(600, 50),
    Objeto(805, 36),
    Objeto(430, 25),
    Objeto(1200, 64),
    Objeto(770, 54),
    Objeto(60, 18),
    Objeto(930, 46),
    Objeto(353, 28),
]

# Numero de objetos, dato dado por el enunciado
n = len(objetos)

# Capacidad o volumen maximo soportado por la mochila, dato dado por el enunciado
capacidad = 4200

# Lista de la solucion, cada posicion de esta lista coincide con la posicion del objeto en la lista objetos
# En una etapa inicial o intermedia todos o algunos de los elementos de la lista seran None (incertidumbre)
# Si meto un objeto a la mochila se simboliza con un True si no lo guardo se simboliza con un False
# Por ejemplo si mi lista solucion es [False, False, True, True, False, False, False, False, True, True] 
# significa que guarde en mi mochila los objetos objetos[2], objetos[3], objetos[8] y objetos[9]
solucion = [None for i in range(10)]

# En esta lista se guardaran todas las soluciones finales validas al problema
# Esta lista es sometida a un ordenamiento para ordenar de la mejor a la peor
# solucion segun el valor total de los objetos guardados en la mochila
soluciones = []

# Hay 2^10 = 1024 soluciones si no se aplica ninguna restriccion,
# hay que ver cuantas quedan luego de aplicada la restriccion

# Funcion encargada de buscar las soluciones y en caso de que sean soluciones
# validas y finales del problema, guardarlas en una lista de soluciones
# toma como parametros una lista solucion la cual es la solucion parcial del
# problema, la lista de objetos, necesaria para validar la solucion obtenida
# y la etapa de la solucion, que indica sobre cual objeto se esta decidiendo
# si guardarlo o no en la mochila. Por ejemplo, en la etapa 0 (la inicial)
# se esta decidiendo si guardar el primer objeto o no; en la etapa 1, se
# decide sobre el segundo, en la 2 sobre el tercero, y asi sucesivamente. 
def buscarSolucion(solucion: list, objetos: list, etapa: int = 0):
    loGuardo: bool = False

    if etapa > n - 1:
        return

    while True:
        # Se crea una copia de la solucion para que al guardarla en la
        # lista de soluciones, los cambios realizados en esta se vean 
        # reflejados fuera de la funcion buscarSolucion, de lo contrario 
        # al imprimir la lista soluciones fuera de la funcion, todas las
        # soluciones que se encuentran guardadas tienen solo elementos
        # None, que es el estado inicial de las soluciones.
        # En resumen, todas las soluciones seran como la de abajo.
        # [None, None, None, None, None, None, None, None, None, None]     
        solucionCopia = solucion.copy()
        solucionCopia[etapa] = loGuardo

        # Chequea que la solucion parcial sea una solucion valida
        # de no cumplir con las condiciones dadas se prueba con otro
        # valor de loGuardo, que simboliza si guarda o no el objeto
        if (validarSolucion(solucionCopia, objetos, etapa)):
            # Chequea si la solucion actual es una solucion final al
            # comparar la etapa con el numero de objetos menos uno
            if (etapa == n - 1):
                # Se guarda la solucion valida en la lista de soluciones
                guardarSolucion(solucionCopia, soluciones)
                ordenarSoluciones(soluciones, objetos)
            else:
                # Al no ser una solucion final, se decide sobre el siguiente objeto 
                buscarSolucion(solucionCopia, objetos, etapa + 1)
        
        loGuardo = not loGuardo
        if solucionCopia[etapa]: 
            break
        
    solucion[etapa] = None

# Esta funcion tiene la tarea de devolver un booleano que simbolice
# si la solucion cumple con las restricciones.
# Devolvera True si el valor total de los objetos guardados indicados
# en la solucion es menor a 4200 (valor indicado en el enunciado)
def validarSolucion(solucion: list, objetos: list, etapa: int) -> bool:
    i = 0
    total = 0
    while i <= etapa:
        if solucion[i]:
            total += objetos[i].volumen
        i += 1

    return total <= capacidad

# Simplemente guarda la solucion en la lista de soluciones como
# un objeto con las propiedades: solucion y total, esta ultima
# propiedad es posteriormente calculada en el ordenamiento
def guardarSolucion(solucion: list, soluciones: list):
    soluciones.append({"solucion": solucion, "total": 0 })

# Ordena la lista de soluciones de la mejor a la peor
# segun el valor total de los objetos guardados
def ordenarSoluciones(soluciones: list, objetos: list):
    for solucion in soluciones:
        solucion["total"] = obtenerTotal(solucion["solucion"], objetos)
    soluciones.sort(key=obtenerTotalSolucion, reverse=True)

# Obtiene el valor total de los objetos indicados por la solucion
def obtenerTotal(solucion: list, objetos: list):
    total = 0
    for i, guardado in enumerate(solucion):
        if guardado:
            total += objetos[i].valor
    return total

# Funcion utilizada en el ordenamiento de la lista soluciones
# devuelve el valor total de la solucion
def obtenerTotalSolucion(solucion):
    return solucion["total"]

# Ejecucion

buscarSolucion(solucion, objetos)

for solucion in soluciones:
    print(solucion["solucion"], "Valor:", solucion["total"], "\n")
    
    # Podriamos mostrar los datos como hicimos con el primer TP
    # usando la libreria de openxls 
