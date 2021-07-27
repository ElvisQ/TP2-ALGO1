import os
import service_drive
from apiclient.http import MediaFileUpload
from auxiliar import SERV_DR

def subir(ruta_archivo:list, id_carpeta:str, mimetype:str)-> None:
    """
    Sube los archivos a Drive.
    """
    for archivos in ruta_archivo:
        file_metadata = {'name': archivos, 'parents': [id_carpeta]}
        media = MediaFileUpload(archivos, mimetype=mimetype)
        file = SERV_DR.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()

def tipos_archivos()->str:
    """
    Le pregunta al usuario que tipo de archivo desea manejar.
    """
    tipo = ['text/plain', 'text/csv', 'application/json', 'application/zip','application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
    print("---------Ingrese que tipo de archivo desea---------")
    print("1. .txt")
    print("2. .csv")
    print("3. .json")
    print("4. .zip")
    print("5. .pdf")
    print("6. .docx")
    opcion = input("Ingrese una opción: ")
    while not (opcion.isnumeric()):
        opcion = input("Error! Ingrese una opción válida: ")
    opcion = int(opcion)
    opciones = opcion - 1
    tipo_archivo = tipo[opciones]
    return tipo_archivo
    

def parametros()-> tuple: 
    """
    Le pedirá al usuario los datos correspondientes para subir el archivo.
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

#main del programa
def archivo_subido()-> None:
    mimetype = tipos_archivos()
    ruta_archivo, id_carpeta = parametros()
    subir(ruta_archivo, id_carpeta, mimetype)
