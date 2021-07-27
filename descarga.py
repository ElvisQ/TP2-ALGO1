 import io, os
from googleapiclient.http import MediaIoBaseDownload
from auxiliar import RUTA, SERV_DR, EXPORT

def descargar(nombre_archivo: str, id_archivo: str, tipo_archivo: str) -> None:
    '''
    PRE: Recibe el nombre, id, y tipo del archivo elegido por el usuario.
    POST: Descarga el archivo solicitado.
    '''
    if tipo_archivo in EXPORT:
        tipo_exportado = EXPORT[tipo_archivo]
        request = SERV_DR.files().export_media(fileId=id_archivo,mimeType=tipo_exportado)
    else:
        request = SERV_DR.files().get_media(fileId=id_archivo)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    fh.seek(0)
    with open(os.path.join(RUTA,nombre_archivo), 'wb') as f:
        f.write(fh.read())
        f.close()
    print("Se ha descargado {0}".format(nombre_archivo))

def verificar_existencia(nombre: str) -> tuple:
    '''
    PRE: Recibe el nombre de un archivo.
    POST: Verifica que el nombre de archivo ingresado exista en el Drive del usuario. Si existe, llama a la función 'descargar'.
    '''
    datos_archivos = (1,1,1) #si datos queda (1,1,1) es porque no existe el archivo ingresado.
    print("Verificando coincidencias, puede demorar...")
    archivos_coincidentes = SERV_DR.files().list(fields='nextPageToken, files(id, name, mimeType, modifiedTime, parents)').execute()
    lista_archivos = archivos_coincidentes.get('files')
    nextPageToken = archivos_coincidentes.get('nextPageToken')
    while nextPageToken:
        archivos_coincidentes = SERV_DR.files().list(fields='nextPageToken, files(id, name, mimeType, modifiedTime, parents)',pageToken=nextPageToken).execute()
        lista_archivos.extend(archivos_coincidentes.get('files'))
        nextPageToken = archivos_coincidentes.get('nextPageToken')
    for i in range(len(lista_archivos)):
        if lista_archivos[i]['name'] == nombre:
            datos_archivos = (nombre,lista_archivos[i]['id'],lista_archivos[i]['mimeType'])
    return datos_archivos

def input_archivo() -> tuple:
    '''
    POST: Pide al usuario ingresar un nombre de archivo. Si el usuario ingresa ENTER o una cadena de espacios, vuelve al menú. Caso contrario el programa procede a verificar la existencia del archivo.
    '''
    datos_archivos = (0,0,0) #si datos queda (0,0,0) se vuelve al menú.
    condicion_salida = True
    archivo = input("\nIngrese el nombre del archivo que quiere descargar. Presione ENTER o deje espacios para volver al menú.\n")
    for i in archivo:
        if i.isalnum():
            condicion_salida = False
    if not condicion_salida:
        datos_archivos = verificar_existencia(archivo)
    return datos_archivos
        
def main_descarga() -> None:
    resultados = input_archivo()
    if resultados == (1,1,1): #archivo inexistente
        respuesta = input("El archivo ingresado no existe. ¿Reintentar? (s/n) ")
        while respuesta != "s" and respuesta != "n":
            respuesta = input("Entrada no válida. ¿Reintentar? (s/n) ")
        if respuesta == "s":
            main_descarga()
    elif resultados != (1,1,1) and resultados != (0,0,0): #archivo encontrado
        descargar(resultados[0],resultados[1],resultados[2])
