from compartidos import *
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Side, Border
import os


# Especifica el directorio donde se guardara el archivo Excel con las posibles soluciones
# Estas se encuentran ordenas de mejor a peor
directorio_resultados = "resultados"

# Verifica si el directorio existe, de no existir se creara
if not os.path.exists(directorio_resultados):
    os.makedirs(directorio_resultados)


paso = input("¿Desea realizar el punto 1, 2 o 3?\n")
while (paso != "1" and paso != "2" and paso != "3"):
    utilizaElitismo = input("¿Desea realizar el punto 1, 2 o 3?\n")

if (paso == "1" or paso == "2"):
    objetos: list = [
        Objeto(150, 0, 20),
        Objeto(325, 0, 40),
        Objeto(600, 0, 50),
        Objeto(805, 0, 36),
        Objeto(430, 0, 25),
        Objeto(1200, 0, 64),
        Objeto(770, 0, 54),
        Objeto(60, 0, 18),
        Objeto(930, 0, 46),
        Objeto(353, 0, 28),
    ]
    # Capacidad o volumen maximo soportado por la mochila, dato dado por el enunciado
    capacidad = 4200

elif paso == "3":
    # Datos de los objetos dados por el enunciado
    objetos: list = [
        Objeto(0, 1800, 72),
        Objeto(0, 600, 36),
        Objeto(0, 1200, 60)
    ]
    # Capacidad maxima soportada por la mochila, dato dado por el enunciado
    capacidad = 3000

# Lista de la solucion, cada posicion de esta lista coincide con la posicion del objeto en la lista objetos
# En una etapa inicial o intermedia todos o algunos de los elementos de la lista seran None (incertidumbre)
# Si meto un objeto a la mochila se simboliza con un True si no lo guardo se simboliza con un False
# Por ejemplo si mi lista solucion es [False, False, True, True, False, False, False, False, True, True] 
# significa que guarde en mi mochila los objetos objetos[2], objetos[3], objetos[8] y objetos[9]
solucion = [None for i in range(len(objetos))]



# En esta lista se guardaran todas las soluciones finales validas al problema
# Esta lista es sometida a un ordenamiento para ordenar de la mejor a la peor
# solucion segun el valor total de los objetos guardados en la mochila
#Si no se aplican restricciones habria 2^n soluciones, siendo "n" la cantidad de objetos disponibles
#El numero decrece mucho si se aplican restricciones
soluciones = []


buscarSolucion(solucion, objetos, capacidad, soluciones)
ordenarSoluciones(soluciones, objetos)


# Guardado de archivo xls

# Crear un nuevo libro de Excel
libro_excel = Workbook()
hoja_excel = libro_excel.active
hoja_excel.title = f"Soluciones de la Mochila"

bordeDelgado = Side(border_style="thin", color="000000")

#Tamaño columnas
hoja_excel.column_dimensions["A"].width = 55
hoja_excel.column_dimensions["B"].width = 15

# Encabezados
hoja_excel['A1'] = f"Paso {paso}"
hoja_excel['A1'].font = Font(bold=True)
alinearCelda(hoja_excel['A1'])
ponerBorde(hoja_excel['A1'], bordeDelgado)

hoja_excel['A2'] = "Solución"
hoja_excel['A2'].font = Font(bold=True)
alinearCelda(hoja_excel['A2'])
ponerBorde(hoja_excel['A2'], bordeDelgado)

hoja_excel['B2'] = "Valor total"
hoja_excel['B2'].font = Font(bold=True)
alinearCelda(hoja_excel['B2'])
ponerBorde(hoja_excel['B2'], bordeDelgado)

hoja_excel.merge_cells('A1:B1')


# Llenar la hoja de cálculo con las soluciones y sus valores
for indice, solucion in enumerate(soluciones):
    fila = indice + 3  # Empezar desde la fila 3, ya que la primera fila contiene encabezados
    hoja_excel[f'A{fila}'] = str(solucion["solucion"])
    ponerBorde(hoja_excel[f'A{fila}'], bordeDelgado)
    alinearCelda(hoja_excel[f'A{fila}'])
    
    hoja_excel[f'B{fila}'] = solucion["total"]
    ponerBorde(hoja_excel[f'B{fila}'], bordeDelgado)
    alinearCelda(hoja_excel[f'B{fila}'])


# Guardar el libro de Excel en el directorio de resultados
nombre_archivo_excel = f"soluciones Mochila Paso {paso}.xlsx"
ruta_archivo_excel = os.path.join(directorio_resultados, nombre_archivo_excel)
libro_excel.save(ruta_archivo_excel)

print(f"Se han guardado las soluciones en '{ruta_archivo_excel}'")