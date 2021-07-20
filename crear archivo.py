from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

GAUTH = GoogleAuth()
GAUTH.LocalWebserverAuth()
DRIVE = GoogleDrive(GAUTH) 

def crear_archivo_drive (nombre_archivo: str, id_carpeta:str)-> None:
    """
    Crea los archivos en drive
    """

    archivo = DRIVE.CreateFile({'title': nombre_archivo, 'parents': [{'kind': 'drive#linkArchivo', 'id': id_carpeta}]} )
    archivo.Upload()
 

def parametros_archivo()-> tuple:
    """
    Le pide al usuario los datos necesarios para crear el archivo
    """

    nombre_archivo = input("Ingrese el nombre del archivo: ")

    extension = input("Ingrese la extension (incluyendo el '.'): ")

    nombre_completo = nombre_archivo + extension
    
    print("Se le pedirá que ingrese el 'id' de la carpeta, para hacerlo copie desde el url")
    opcion = input("¿Desea ver un ejemplo? <s/n>: ")

    if opcion != "n":
        print("Por ejemplo, usted posee un URL: drive.google.com/drive/u/2/folders/108lNDFnBijidpS1mooGsk8s6fr4V76pS")
        print("La ID de su carpeta será 108lNDFnBijidpS1mooGsk8s6fr4V76pS")

    id_carpeta = input("Ingrese el ID de su carpeta: ")
    return nombre_completo, id_carpeta

def crear()-> None:
    nombre_archivo, id_carpeta = parametros_archivo()
    nuevo_archivo = open(nombre_completo, 'a') #Crea los archivos en remoto
    crear_archivos(nombre_archivo, id_carpeta)
crear()