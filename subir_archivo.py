from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

client_secret = 'client_secrets.json'
token = 'token_drive.json'
gauth = GoogleAuth()
  
drive = GoogleDrive(gauth)  

#sube el archivo
def subir_archivo()-> None: 
    ruta_archivo, id_carpeta = parametros()
    for archivos in ruta_archivo:
        archivo = drive.CreateFile({'parents': [{'id': id_carpeta}]})
        archivo.SetContentFile(archivos)
        archivo.Upload()

   
def parametros ():
    ruta_archivo = []
    print()
    nombre_archivo = input("Ingrese el nombre completo del archivo: ")
    ruta_archivo.append(nombre_archivo)
    print()
    id_carpeta = input("Ingrese el ID de su carpeta de Drive: ")

    return ruta_archivo, id_carpeta


def main():
    subir_archivo()
main()
