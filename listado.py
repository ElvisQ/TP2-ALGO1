import os
from os.path import isfile, join

ESPACIOS = '''Donde desea buscar?
1. Archivos en carpeta local.
2. Archivos en carpeta remota
'''
RUTA = os.getcwd()

def elegir_espacio() -> int:
#Printea las opciones y pide al usuario que elija una. Luego, la devuelve.
    print(ESPACIOS)
    espacio_elegido = input("Elija una opcion: ")
    while not espacio_elegido.isnumeric():
        espacio_elegido = input("Debe ingresar un numero. Elija una opcion: ")
    return int(espacio_elegido)

def listar_local() -> None:
#Lista los archivos de la carpeta local actual.
    contenido = os.listdir(RUTA)
    archivos = [nombre for nombre in contenido if isfile(join(RUTA,nombre))]
    print(archivos)

def listar_remoto():
#Lista los archivos de la carpeta remota actual.
    print("listar remoto")

def ejecutar_listado(espacio: int) -> None:
#Recibe una opcion numerica y ejecuta una funcion segun lo elegido.
    if espacio == 1:
        listar_local()
    elif espacio == 2:
        listar_remoto()
    else:
        print("Esa opcion no existe")
        espacio_elegido = elegir_espacio() 
        ejecutar_listado(espacio_elegido)

def main_listado() -> None:
    espacio_elegido = elegir_espacio()
    ejecutar_listado(espacio_elegido)