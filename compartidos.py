from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Side, Border

########################## Funciones mas que nada para metodo exhaustivo ##########################

# Un objeto con un peso (int) en gramos y un valor (int)
class Objeto:
    def __init__(self, volumen: int= 0,peso: int = 0, valor: int = 0) -> None:
        self.peso = peso
        self.volumen = volumen
        self.valor = valor
        if self.volumen !=0:
            self.indice = round(valor / volumen, 4)
        else:
            self.indice = round(valor / peso, 4)

    def __repr__(self) -> str:
        if self.volumen !=0:
            return f"\nVolumen: {self.volumen} - Valor: {self.valor} - Indice: {self.indice}"
        else:
            return f"\nPeso: {self.peso} - Valor: {self.valor}"


# Esta funcion tiene la tarea de devolver un booleano que simbolice
# si la solucion cumple con las restricciones del enunciado.
# Devolvera True si el valor total de los objetos guardados indicados
# en la solucion es menor al valor indicado en el enunciado
def validarSolucion(solucion: list, objetos: list, etapa: int, capacidad) -> bool:
    i = 0
    total = 0
    while i <= etapa:
        if solucion[i]:
            #Si el volumen es igual a 0 significa que estoy evaluando el problema
            #segun el peso de los objetos y no segun su volumen
            if objetos[i].volumen == 0:
                total += objetos[i].peso
            else:
                total += objetos[i].volumen
        i += 1

    return total <= capacidad


# Ordena la lista de soluciones de la mejor a la peor
# segun el valor total de los objetos guardados
def ordenarSoluciones(soluciones: list, objetos: list):
    for solucion in soluciones:
        solucion["total"] = obtenerTotal(solucion["solucion"], objetos)
    soluciones.sort(key=lambda x: x['total'], reverse=True)


# Obtiene el valor total de los objetos indicados por la solucion
def obtenerTotal(solucion: list, objetos: list):
    total = 0
    for i, guardado in enumerate(solucion):
        if guardado:
            total += objetos[i].valor
    return total

# Simplemente guarda la solucion en la lista de soluciones como
# un objeto con las propiedades: solucion y total, esta ultima
# propiedad es posteriormente calculada en el ordenamiento
def guardarSolucion(solucion: list, soluciones: list):
    soluciones.append({"solucion": solucion, "total": 0 })



# Funcion encargada de buscar las soluciones y en caso de que sean soluciones
# validas y finales del problema, guardarlas en una lista de soluciones
# toma como parametros una lista solucion la cual es la solucion parcial del
# problema, la lista de objetos, necesaria para validar la solucion obtenida
# y la etapa de la solucion, que indica sobre cual objeto se esta decidiendo
# si guardarlo o no en la mochila. Por ejemplo, en la etapa 0 (la inicial)
# se esta decidiendo si guardar el primer objeto o no; en la etapa 1, se
# decide sobre el segundo, en la 2 sobre el tercero, y asi sucesivamente. 
def buscarSolucion(solucion: list, objetos: list, capacidad, soluciones, etapa: int = 0):
    # Numero de objetos, dato dado por el enunciado
    n = len(objetos)

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
        if (validarSolucion(solucionCopia, objetos, etapa, capacidad)):
            # Chequea si la solucion actual es una solucion final al
            # comparar la etapa con el numero de objetos menos uno
            if (etapa == n - 1):
                # Se guarda la solucion valida en la lista de soluciones
                guardarSolucion(solucionCopia, soluciones)
            else:
                # Al no ser una solucion final, se decide sobre el siguiente objeto 
                buscarSolucion(solucionCopia, objetos, capacidad, soluciones, etapa + 1)
        
        loGuardo = not loGuardo
        if solucionCopia[etapa]: 
            break
        
    solucion[etapa] = None


########################## Funciones sobre metodo heuristico ##########################

def ordenarObjHeu(objetos):
    # Ordena la lista de objetos segun su indice
    # el argumento 'key' simboliza segun que
    # valor se ordenaran los elementos
    objetos.sort(key=lambda x: x.indice, reverse=True)


# Devuelve el valor total de una mochila, realizando una
# sumatoria sobre los valores de todos los objetos guardados en la misma 
def obtenerTotalHeu(mochila) -> int:
    total = 0
    for objeto in mochila:
        total += objeto.valor
    return total


def buscarSolucionHeu(objetos: list, capacidad: int):
    n = len(objetos)
    mochila= []
    capacidadRestante = capacidad
    i = 0
    
    # Se realiza el ordenamiento de los objetos segun su indice de mayor a menor
    ordenarObjHeu(objetos)

    # Mientras haya objetos seguira recorriendo la lista de objetos
    while(i < n):
        # Si el objeto actual cabe en la mochila lo guardara en ella
        if objetos[i].volumen != 0:
            if (capacidadRestante >= objetos[i].volumen):
                mochila.append(objetos[i])
                # Disminuye la capacidad restante de la mochila
                capacidadRestante -= objetos[i].volumen
        else:
            if (capacidadRestante >= objetos[i].peso):
                mochila.append(objetos[i])
                # Disminuye la capacidad restante de la mochila
                capacidadRestante -= objetos[i].peso

        i += 1
    # Devuelve una lista con los objetos guardados y el valor total de los objetos guardados
    return [mochila, obtenerTotalHeu(mochila)]



########################## Funciones sobre excel ##########################

def alinearCelda(celda):
    celda.alignment = Alignment(horizontal='center')

def ponerBorde(celda, borde):
    celda.border = Border(top=borde, left=borde, right=borde, bottom=borde)