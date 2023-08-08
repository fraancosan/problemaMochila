# Un objeto con un volumen (int) y un valor (int)
#
# AGREGADO EN INCISO 2)
#
# Se agrego la propiedad indice (float)
# que es una medida de lo factible que resulta guardar el objeto
# en la mochila diviendo el valor por su volumen    
class Objeto:

    def __init__(self, volumen: int, valor: int) -> None:
        self.volumen = volumen
        self.valor = valor
        self.indice = round(valor / volumen, 4)

    def __repr__(self) -> str:
        return f"\nVolumen: {self.volumen} - Valor: {self.valor} - Indice: {self.indice}"
    
# Datos de los objetos dados por el enunciado
OBJETOS: list[Objeto] = [
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
N = len(OBJETOS)

# Capacidad o volumen maximo soportado por la mochila, dato dado por el enunciado
CAPACIDAD = 4200

# Funcion encargada de buscar la mejor solucion utilizando el algoritmo greedy
# Se le debera pasar la lista de objetos la capacidad de la mochila y la cantidad
# de objetos disponibles para elegir.
# Se ordena la lista de objetos segun su indice (valor / volumen) y se van guardando
# en orden en la lista llamada mochila validando la capacidad restante de la misma
def buscarSolucionGreedy(objetos: list[Objeto], capacidad: int, cantidadObjetos: int) -> dict[list, int]:
    mochila: list = []
    capacidadRestante = capacidad
    i = 0

    # Se realiza el ordenamiento de los objetos segun su indice de mayor a menor
    ordenarObjetos(objetos)

    # Mientras haya objetos seguira recorriendo la lista de objetos
    while(i < cantidadObjetos):

        # Si el objeto actual cabe en la mochila lo guardara en ella
        if (capacidadRestante >= objetos[i].volumen):
            mochila.append(objetos[i])
            # Disminuye la capacidad restante de la mochila
            capacidadRestante -= objetos[i].volumen
        
        i += 1
    
    # Devuelve una lista con los objetos guardados y el valor total de los objetos guardados
    return {"mochila": mochila, "total": obtenerTotal(mochila)}

# Ordena la lista de objetos segun su indice
def ordenarObjetos(objetos: list[Objeto]):
    # Metodo utilizado para ordenar listas,
    # el argumento 'key' simboliza segun que
    # valor se ordenaran los elementos
    objetos.sort(key=obtenerIndiceObjeto, reverse=True)

# Devuelve el indice de los objetos, funcion util para realizar
# el ordenamiento segun el metodo sort 
def obtenerIndiceObjeto(objeto: Objeto) -> float:
    return objeto.indice

# Devuelve el valor total de una mochila, realizando una
# sumatoria sobre los valores de todos los objetos guardados en la misma 
def obtenerTotal(mochila: list[Objeto]) -> int:
    total = 0
    for objeto in mochila:
        total += objeto.valor
    return total

# Ejecucion

solucion: dict[list, int] = buscarSolucionGreedy(OBJETOS, CAPACIDAD, N)

print(solucion)

# Podemos agregar el resultado del greedy al XLS creado por la parte 1)
# y asi mostrar todo en el mismo documento 