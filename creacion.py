import os

POSIBLES_EXTENSIONES = '''\n¿Qué tipo de archivo desea crear?\n
1. Carpeta.
2. .txt
3. .csv
4. .zip
5. .pdf
'''

def elegir_extension() -> int:
    '''
    Printea las extensiones y pide al usuario que elija una. Luego, la devuelve.
    '''
    print(POSIBLES_EXTENSIONES)
    extension_elegida = input("Elija una opcion: ")
    while not extension_elegida.isnumeric():
        extension_elegida = input("Debe ingresar un numero. Elija una opcion: ")
    return int(extension_elegida)
    
def crear_carpeta():
    nombre = input('Ingrese nombre de carpeta: ')
    if os.path.exists(nombre):
        print('Ya existe una carpeta con ese nombre')
    else:
        os.mkdir(nombre)

def crear_txt():
    print("hola")

def crear_csv():
    print("hola")

def crear_zip():
    print("hola")

def crear_pdf():
    print("hola")

def ejecutar_creacion(extension: int) -> None:
    '''
    Recibe una extensión elegida y ejecuta una funcion según lo elegido.
    '''
    if extension == 1:
        crear_carpeta()
    elif extension == 2:
        crear_txt()
    elif extension == 3:
        crear_csv()
    elif extension == 4:
        crear_zip()
    elif extension == 5:
        crear_pdf()
    else:
        print("Esa opcion no existe")
        extension_elegida = elegir_extension() 
        ejecutar_creacion(extension_elegida)

def main_creacion() -> None:
    extension = elegir_extension()
    ejecutar_creacion(extension)
