import os, subida
from auxiliar import SERV_DR

def validar_existencia(nombre_archivo:str)->str:
    """
    Pre: Toma el nombre del archivo.
    Post: Verifica que no exista un archivo con el mismo nombre, en caso de que exista, 
    devolverá el nuevo nombre del archivo.
    """
    while (os.path.isfile(nombre_archivo)) == True:
        print("Error! ya existe un archivo con ese nombre")
        nombre_archivo = input("Ingrese uno nuevo con su respectiva extension: ")
    return nombre_archivo

def parametros_archivo()-> tuple:
    """
    Pre: ----
    Post: Le pide al usuario los datos necesarios para crear el archivo y los devuele.
    """
    archivo = []

    mimetype = subir_archivo.tipos_archivos()

    nombre_archivo = input("Ingrese el nombre del archivo incluyendo la extension '.': ")

    nombre_archivo = validar_existencia(nombre_archivo)
    
    archivo.append(nombre_archivo)

    print("Se le pedirá que ingrese el 'id' de la carpeta, para hacerlo copie desde el url")
    opcion = input("¿Desea ver un ejemplo? <s/n>: ")

    if opcion != "n":
        print("Por ejemplo, usted posee un URL: drive.google.com/drive/u/2/folders/108lNDFnBijidpS1mooGsk8s6fr4V76pS")
        print("La ID de su carpeta será 108lNDFnBijidpS1mooGsk8s6fr4V76pS")

    id_carpeta = input("Ingrese el ID de su carpeta: ")
    return archivo, id_carpeta, mimetype


def crear()-> None:
    """
    Pre: ---
    Post: Crea el archivo en remoto y llama a la funcion de subir archivo para que sea subido a Drive.
    """
    nombre_archivo, id_carpeta, mimetype = parametros_archivo()

    archivo = nombre_archivo[0]

    nuevo_archivo = open(archivo, 'a') #Crea los archivos en remoto

    subida.subir(nombre_archivo, id_carpeta, mimetype)
