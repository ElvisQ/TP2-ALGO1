import mimetypes, os, time, datetime, io
from pathlib import Path
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from auxiliar import RUTA, SERV_DR, EXPORT


def enlistar_carpetas_drive(servicio_drive:any) -> dict:
    '''
    PRE: recibe el servicio de drive
    POST: retorna un diccionario con keys igual a los nombres de las carpetas en drive
          con valor igual a sus respectivos id's
    '''
    nombre_carpeta_id = {}  # {nombre:id}
    resultado = servicio_drive.files().list(
        q="mimeType= 'application/vnd.google-apps.folder' and 'me' in owners and trashed=false",
        fields="nextPageToken,files(id,name, createdTime, modifiedTime, mimeType)").execute()

    datos = resultado.get('files', [])
    for i in datos:

        nombre_carpeta_id[i['name']]=(i['id'])

    return nombre_carpeta_id


def buscar_hora_modificacion(archivo: str,direccioncarpeta:str)->any:
    '''
    PRE: Recibe el nombre del archivo a obtener fecha de modificacion y la ruta
    POST: Retorna la fecha de ultima modificacion del archivo
    '''

    ruta=os.path.join(direccioncarpeta,archivo)
    estado = os.stat(ruta).st_mtime

    fecha = time.localtime(estado)

    fecha = datetime.datetime(fecha[0], fecha[1], fecha[2], fecha[3], fecha[4], fecha[5])

    return fecha


def cambiar_formato_mod_drive(carpeta:str, archivo:str, servicio:any,carpetaiddrive:dict)->any:
    '''
    PRE: Recibe el nombre de la carpeta y  archivo , el servicio de drive y el diccionario "carpeta:id"
    POST: Retorna el horario pero en horario local
    '''

    query=f"parents ='{carpetaiddrive[carpeta]}'"
    resultado=servicio.files().list(q=query,fields="nextPageToken, files(name, id, modifiedTime)").execute()

    files=resultado.get('files',[])
    mt=""
    for i in files:
        nombre=i['name']
        if nombre==archivo:
            mt=i['modifiedTime']

    dt = datetime.datetime.strptime(mt, "%Y-%m-%dT%H:%M:%S.%fZ")  # ->datetime

    cambio_formato = dt.strftime("%Y-%m-%d %H:%M:%S")  # ->str

    final = datetime.datetime.strptime(cambio_formato, "%Y-%m-%d %H:%M:%S")  # ->datetime
    horario_local = time.time()
    diferencia = datetime.datetime.fromtimestamp(horario_local) - datetime.datetime.utcfromtimestamp(horario_local)

    utc_a_local = final + diferencia

    return utc_a_local


def buscar_id_archivo(nombre_archivo:str, servicio:any)->str:
    '''
    PRE:Recibe el nombre del archivo y el servicio de drive
    POST:Retotrna el Id del archivo
    '''
    resultado = servicio.files().list(q=f"name= '{nombre_archivo}'").execute()

    files = resultado.get('files', [])
    id = files[0]['id']

    return id


def buscar_id_carpeta(nombre: str, servicio:any)->str:
    '''
    PRE:Recibe el nombre de la carpeta y el servicio de drive
    POST:Retorna el Id de la carpeta
    '''

    query=f"name = '{nombre}'"
    resultado = servicio.files().list(q=query).execute()
    files = resultado.get('files', [])

    id = files[0]['id']
    return id


def obtenermime(servicio:any, archivo:str)->str:
    '''
    PRE:Recibe el servicio de drive junto con el nombre del archivo
    POST: Retorna el MimeType del archivo en drive
    '''

    resultado = servicio.files().list(q=f"name='{archivo}'").execute()

    files = resultado.get('files', [])
    mime = files[0]['mimeType']
    return mime


def actualizar_archivo_en_drive(archivo_nombre: str, servicio:any, ruta_archivo:str)->None:
    '''
    PRE: Recibe el nombre del archivo, el servicio de drive y la ruta completa del archivo
    POST:Sube a Drive el archivo en su respectiva carpeta
    '''
    nombre_de_la_carpeta=ruta_archivo.split("\\")
    id = buscar_id_carpeta(nombre_de_la_carpeta[-2], servicio)

    tipo_dato = mimetypes.guess_type(ruta_archivo)
    file_metadata = {
        'name': archivo_nombre,
        'mimeType': tipo_dato[0],
        'parents': [id]
    }

    contenido = MediaFileUpload(ruta_archivo, mimetype=tipo_dato[0], resumable=True)
    servicio.files().create(body=file_metadata, media_body=contenido, fields='id').execute()
    print(f'archivo{archivo_nombre} actualizado\n')

def descargar_archivos(nombre_de_archivo:str, servicio:any, ruta_archivo,tipo_archivo:str)->None:
    '''
    PRE:Recibe el nombre del archivo el servicio de drive la ruta del archivo y su MimeType
    POST:Descarga el archivo de drive a la ruta especificada
    '''
    id = buscar_id_archivo(nombre_de_archivo, servicio)
    if tipo_archivo in EXPORT:
        tipo_exportado = EXPORT[tipo_archivo]
        resultado = servicio.files().export_media(fileId=id, mimeType=tipo_exportado)
    else:
        resultado = servicio.files().get_media(fileId=id)

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, resultado)
    completado = False
    while not completado:
        estado, completado = downloader.next_chunk()
        print(f'descargando... {estado.progress() * 100}')
    with io.open(ruta_archivo, 'wb')as file:
        fh.seek(0)
        file.write(fh.read())
        file.close()


def listar_archivos_drive(servicio:any, carpetasdict:dict, nombre_carpeta:str)->dict:
    '''
    PRE: Recibe el servicio de drive, el diccionario con keys com los nombres de las carpetas en drive
         y como valores sus respectivos Id's, y el nombre de la carpeta a listar los archivos
    POST:Retorna un diccionario con el nombre del archivo como key y la fecha de modificacion como valor
    '''
    lista_archivos_modificacion = {}
    id_actual = carpetasdict[nombre_carpeta]
    query = f"parents= '{id_actual}'"
    respuesta = servicio.files().list(q=query,
                                      fields="nextPageToken,files(id,name, createdTime, modifiedTime, mimeType)").execute()

    files = respuesta.get("files", [])

    for file in files:
        lista_archivos_modificacion[file['name']] = file['modifiedTime']
    return lista_archivos_modificacion

def comparar_fecha_modificacion(lista_archivos_coincidentes:list, lista_ruta_archivos:list, dir_carpeta:str,carpetas_ids_drive:dict,servicio:any,archivos_act_local:list,archivos_act_drive:list)->None:
    '''
    PRE:recibe la lista de archivos coincidentes, la lista de las rutas de los archivos en cuestion, el directorio de la carpeta, el diccionario 'carpeta:id', el servicio de drive, y las dos listas de los archivos actualizados, local y remoto.
    POST: segun la feecha de modificaion de los archivos se actualizara o en local o en remoto
    '''
    carpeta_del_archivo=dir_carpeta.split('\\')
    for archivo in lista_archivos_coincidentes:
        # como el archivo coincide en ambos lugares debo verificar cual fue modificado mas recientemente
        modificacion_de_archivo_local = buscar_hora_modificacion(archivo, dir_carpeta)  # ->datetime

        modificacion_de_archivo_remoto = cambiar_formato_mod_drive(carpeta_del_archivo[-1], archivo, servicio,
                                                                   carpetas_ids_drive)  # datetime

        if modificacion_de_archivo_local > modificacion_de_archivo_remoto:
            # significa que esa carpeta en local fue modificada mas recietemente que en remota, por lo tanto esta desactualizada en drive
            for ruta_archivo in lista_ruta_archivos:
                ruta_archivo.split('\\')
                if ruta_archivo[-1] == archivo:
                    actualizar_archivo_en_drive(archivo, servicio, ruta_archivo)
                    archivos_act_drive.append(archivo)

        elif modificacion_de_archivo_local < modificacion_de_archivo_remoto:
            # significa que esa carpeta en remota fue modificada recientemente que en local, por lo tanto esta desactualizada en local
            mime = obtenermime(servicio, archivo)
            for ruta_archivo in lista_ruta_archivos:
                ruta_archivo.split('\\')
                if ruta_archivo[-1] == archivo:
                    descargar_archivos(archivo, servicio, ruta_archivo, mime)
                    archivos_act_local.append(archivo)


def recorrer_archivos_faltantes_drive(lista_faltantes_drive:list,archivos_actualizados_drive:list,lista_rutas_archivos:list,servicio:any)->None:
    '''
    PRE:recibe la lista de archivos faltantes en drive, la list ade archivos ya actualizados en drive, las lista de rutas del o los archivos y el servicio de Drive
    POST:Recorre la lista de los archivos en local y los actualiza en drive
    '''
    for file in lista_faltantes_drive:
        if file not in archivos_actualizados_drive:
            for ruta_archivo in lista_rutas_archivos:
                lista = ruta_archivo.split("\\")
                pathfile = lista[-1]
                if pathfile == file:
                    actualizar_archivo_en_drive(file, servicio, ruta_archivo)
                    archivos_actualizados_drive.append(file)


def recorrer_archivos_faltantes_local(lista_archivos_faltantes_local:list,archivos_actualizados_local:list,lista_ruta_archivos:list,direccion_carpeta:any,servicio:any)->None:
    '''
    PRE: Recibe la lista de archivos faltantes en local, la lista de los archivvos ya actualizados en local,la lista de las rutas de los archivos , la direccion de la carpeta de los archivos y el servicio de Drive
    POST: Recorre la list de los archivos en drive y los descarga en local.
    '''
    for file in lista_archivos_faltantes_local:
        if file not in archivos_actualizados_local:
            if len(lista_ruta_archivos) == 0:
                ruta_descarga = os.path.join(direccion_carpeta, file)
                tipo_mime = obtenermime(servicio, file)
                descargar_archivos(file, servicio, ruta_descarga, tipo_mime)


def comparar_modificaciones(direccion_carpeta: str, carpeta_id_drive: dict, servicio:any, lista_archivos_alumnos:any)->None:
    '''
    PRE:Recibe la direccion de la carpeta local, el diccionario con las carpetas como clave y los id's como valor
        el servicio de drive y la lista de los archivos dentro de la carpeta del alumno
    POST:
    '''
    iterdir= list(lista_archivos_alumnos)
    list_ruta_archivos = []
    sep = direccion_carpeta.split("\\")
    carpeta_del_archivo=sep[-1]
    lista_archivos_local = []

    for dir in iterdir:
        ruta = str(dir)
        archivo = ruta.split('\\')
        list_ruta_archivos.append(ruta)
        lista_archivos_local.append(archivo[-1])

    lista_de_archivos_drive = listar_archivos_drive(servicio, carpeta_id_drive, carpeta_del_archivo)
    #Se lista las comparaciones de los archivos tanto en drive como en local
    lista_de_archivos_coincidentes = list(set(lista_archivos_local).intersection(set(lista_de_archivos_drive)))  # ->esta lista tiene los archivos que existen tanto en drive como en local
    lista_de_archivos_faltantes_en_drive = list(set(lista_archivos_local).difference(lista_de_archivos_drive))  # -> esta lista tiene los archivos que no estan en el drive
    lista_de_archivos_faltantes_en_local = list(set(lista_de_archivos_drive).difference(lista_archivos_local))  # -> esta lista tiene los archivos que no estan en el local

    archivos_actualizados_local = []
    archivos_actualizados_drive = []
    if len(lista_de_archivos_coincidentes) != 0:
        #Como existe el archivo en ambos lugares se debe comparar la fecha de modificacion
        comparar_fecha_modificacion(lista_de_archivos_coincidentes,list_ruta_archivos,carpeta_del_archivo,carpeta_id_drive,servicio,archivos_actualizados_local,archivos_actualizados_drive)
    if len(lista_de_archivos_faltantes_en_drive) != 0:
        #Como hay archivos que no estan en Drive lo actualizo
        recorrer_archivos_faltantes_drive(lista_de_archivos_faltantes_en_drive,archivos_actualizados_drive,list_ruta_archivos,servicio)
    if len(lista_de_archivos_faltantes_en_local) != 0:
        #Como hay archivos que no estan en Local los descargo
        recorrer_archivos_faltantes_local(lista_de_archivos_faltantes_en_local,archivos_actualizados_local,list_ruta_archivos,direccion_carpeta,servicio)



def crear_carpeta_drive(carpeta: str, servicio:any)->None:
    '''
    PRE: Recibe el nombre de la carpeta y el servicio de drive
    POST: Crea la carpeta en google drive
    '''
    file_metadata = {
        'name': carpeta,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    servicio.files().create(body=file_metadata).execute()


def evaluar_carpeta(carpeta_id_drive: dict, carpeta: str, servicio:any)->None:
    '''
    PRE: Recibe el diccionario "carpeta:id",el nombre de la carpeta y el servicio de drive
    POST:
    '''

    if carpeta not in carpeta_id_drive:
        # significa que la carpeta en local no esta en el drive
        # entonces lo creo
        crear_carpeta_drive(carpeta, servicio)
        print(f'la carpeta no se encontraba en drive, Carpeta {carpeta} creada.\n')
    else:
        #si las carpetas se encuentran en ambos lugares debemos buscar la lista de archivos de cada alumno
        lista_de_archivos_en_la_carpeta = Path(os.path.abspath(carpeta)).iterdir()
        if len(os.listdir(carpeta)) != 0:
            for docentee in lista_de_archivos_en_la_carpeta:

                if os.path.isdir(str(docentee)):
                    lista_de_archivos_docentes = Path(str(docentee)).iterdir()
                    if len(os.listdir(str(docentee))) != 0:
                        for alumno in lista_de_archivos_docentes:

                            if os.path.isdir(str(alumno)):
                                lista_de_archivos_alumnos = Path(str(alumno)).iterdir()

                                comparar_modificaciones(str(alumno), carpeta_id_drive, servicio, lista_de_archivos_alumnos)
                            else:
                                print(f"{alumno} no es el directorio tipo parcial\n")
                    else:
                        print(f'\ncarpeta "{docentee}" vacia')
                else:
                    print(f"{docentee} no es el directorio tipo parcial\n")
        else:
            print(f'\ncarpeta "{carpeta}" vacia ')


def sincronizacion(carpeta_id_drive: dict, servicio:any)->None:
    '''
    PRE: Recibe el diccionario carpeta:id y el servicio de drive
    POST:
    '''
    lista_directorio_actual = os.listdir(RUTA)
    lista_directorio_actual.remove('.git')
    lista_directorio_actual.remove('.idea')
    carpetas = 0
    for archivo_carpeta in lista_directorio_actual:
        if os.path.isdir(archivo_carpeta):
            carpetas += 1
            evaluar_carpeta(carpeta_id_drive, archivo_carpeta, servicio)
    else:
        if carpetas == 0:
            print('No hay carpetas , por favor crea alguna')


def main_sinc() -> None:
    carpeta_id = enlistar_carpetas_drive(SERV_DR)

    sincronizacion(carpeta_id, SERV_DR)
