import os
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

GAUTH = GoogleAuth()
GAUTH.LocalWebserverAuth()
DRIVE = GoogleDrive(GAUTH)


def subir_archivo(ruta_archivo:list, id_carpeta:str)-> None: 
    """
    Sube los archivos a drive
    """
    
    for archivos in ruta_archivo:
        archivo = DRIVE.CreateFile({'parents': [{'id': id_carpeta}]})
        archivo.SetContentFile(archivos)
        archivo.Upload()
   
def parametros()-> tuple: 
    """
    Le pedirá al usuario los datos correspondientes para subir el archivo
    """
    ruta_archivo = []

    nombre_archivo = input("Ingrese el nombre completo del archivo o la dirección de ubicación del mismo: ")
    while (os.path.isfile(nombre_archivo)) == False:    #Valida la existencia del archivo
        nombre_archivo = input("Ingrese un nombre válido: ") 
    ruta_archivo.append(nombre_archivo)

    print()
    opcion = input("Se le pedirá que ingrese el ID de la carpeta en el que quiere subir su archivo, desea ver un ejemplo de como hacerlo? <s/n>: ")
    
    if opcion == "s":
        print("----------------EJEMPLO----------------")
        print("Al abrir su carpeta de drive le saldra un url como este: drive.google.com/drive/u/2/folders/108lNDFnBijidpS1mooGsk8s6fr4V76pS ")
        print("El ID de su carpeta será entonces el código que está detrás del ultimo '/' (108lNDFnBijidpS1mooGsk8s6fr4V76pS) ")
    id_carpeta = input("Ingrese el ID de su carpeta de Drive: ")

    return ruta_archivo, id_carpeta


def archivo_subido()-> None:
    ruta_archivo, id_carpeta = parametros()
    subir_archivo(ruta_archivo, id_carpeta)
archivo_subido()
