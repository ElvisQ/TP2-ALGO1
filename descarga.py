import service_drive, io, os
from googleapiclient.http import MediaIoBaseDownload

RUTA_TRABAJO = os.getcwd()

def descargar(nombre_archivo: str, id_archivo: str):
    servicio = service_drive.obtener_servicio()
    print(id_archivo)
    print(nombre_archivo)
    request = servicio.files().get_media(fileId=id_archivo)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

#FUNCION DESCARGAR NO FUNCIONA TODAVÍA


def verificar_existencia(nombre: str) -> tuple:
    '''
    Verifica que el nombre de archivo ingresado exista en el Drive del usuario. Si existe, llama a la función 'descargar'.
    '''
    datos_archivos = (1,1)
    servicio = service_drive.obtener_servicio()
    archivos_coincidentes = servicio.files().list(fields='files(name,id)').execute()
    archivo_encontrado = archivos_coincidentes['files']
    for i in range(len(archivo_encontrado)):
        if archivo_encontrado[i]['name'] == nombre:
            datos_archivos = (nombre,archivo_encontrado[i]['id'])
    print(datos_archivos)
    return datos_archivos

def input_archivo() -> tuple:
    '''
    Pide al usuario ingresar un nombre de archivo. Si el usuario ingresa ENTER o una cadena de espacios, vuelve al menú. Caso contrario el programa procede a verificar la existencia del archivo.
    '''
    datos_archivos = (0,0)
    condicion_salida = True
    archivo = input("\nIngrese el nombre del archivo que quiere descargar. Presione ENTER para volver al menú\n")
    for i in archivo:
        if i.isalnum():
            condicion_salida = False
    if not condicion_salida:
        datos_archivos = verificar_existencia(archivo)
    return datos_archivos
        
def main_descarga() -> None:
    resultados = input_archivo()
    if resultados == (1,1):
        respuesta = input("El archivo ingresado no existe. ¿Reintentar? (s/n) ")
        while respuesta != "s" and respuesta != "n":
            respuesta = input("Entrada no válida. ¿Reintentar? (s/n) ")
        if respuesta == "s":
            main_descarga()
    elif resultados != (1,1) and resultados != (0,0):
        descargar(resultados[0],resultados[1])