import os
import service_drive
import subir_archivo 


def validar_existencia(nombre_archivo:str)-> str:
    """
    Verifica que no exista un archivo con el mismo nombre, en caso de que exista, 
    devolverá el nuevo nombre del archivo.
    """
    while (os.path.isfile(nombre_archivo)) == True:
        print("Error! ya existe un archivo con ese nombre")
        nombre_archivo = input("Ingrese uno nuevo con su respectiva extension: ")
    return nombre_archivo

def parametros_archivo()-> tuple:
    """
    Le pide al usuario los datos necesarios para crear el archivo
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

#main del programa
def crear()-> None:
    nombre_archivo, id_carpeta, mimetype = parametros_archivo()

    archivo = nombre_archivo[0]

    nuevo_archivo = open(archivo, 'a') #Crea los archivos en remoto

    subir_archivo.subir(nombre_archivo, id_carpeta, mimetype)
