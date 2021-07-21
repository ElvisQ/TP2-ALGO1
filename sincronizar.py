import mimetypes
import os
from pathlib import Path
import time
import service_drive
import service_gmail
import datetime
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

RUTA = os.getcwd()
SERIVICO_GMAIL = service_gmail.obtener_servicio()
SERVICIO_DRIVE = service_drive.obtener_servicio()
TIPOS_A_EXPORTAR = {'application/vnd.google-apps.presentation':'application/vnd.oasis.opendocument.presentation',
                    'application/vnd.google-apps.document':'application/pdf',
                    'application/vnd.google-apps.drawing':'image/jpeg',
                    'application/vnd.google-apps.script':'application/vnd.google-apps.script+json',
                    'application/vnd.google-apps.spreadsheet':'application/pdf',
                    'application/vnd.google-apps.jam':'application/pdf',
                    'application/vnd.google-apps.form':'application/pdf',
                    'application/vnd.google-apps.site':'text/plain'
}

def enlistar_carpetas_drive(servicio_drive) -> dict:
    nombre_carpeta_modificacion = {}  # {nombre:fecha_de_modificacion}
    resultado = servicio_drive.files().list(
        q="mimeType= 'application/vnd.google-apps.folder' and 'me' in owners and trashed=false",
        fields="nextPageToken,files(id,name, createdTime, modifiedTime, mimeType)").execute()

    datos = resultado.get('files', [])
    for i in datos:
        print(i)
        nombre_carpeta_modificacion[i['name']] = i['id']
    return nombre_carpeta_modificacion


def buscar_hora_modificacion(carpeta: str):
    print(carpeta)
    estado = os.stat(carpeta).st_mtime
    print(estado)
    fecha = time.localtime(estado)
    print(fecha)
    fecha = datetime.datetime(fecha[0], fecha[1], fecha[2], fecha[3], fecha[4], fecha[5])
    print(fecha)
    return fecha


def cambiar_formato_mod_drive(horario_archivo, servicio):
    dt = datetime.datetime.strptime(horario_archivo, "%Y-%m-%dT%H:%M:%S.%fZ")  # ->datetime

    cambio_formato = dt.strftime("%Y-%m-%d %H:%M:%S")  # ->str

    final = datetime.datetime.strptime(cambio_formato, "%Y-%m-%d %H:%M:%S")  # ->datetime
    horario_local = time.time()
    diferencia = datetime.datetime.fromtimestamp(horario_local) - datetime.datetime.utcfromtimestamp(horario_local)
    print(type(diferencia))
    utc_a_local = final + diferencia

    return utc_a_local


def buscar_id_archivo(nombre_archivo, servicio):
    mime = obtenermime(servicio, nombre_archivo)
    resultado = servicio.files().list(q=f"name= '{nombre_archivo}'").execute()

    print(resultado)
    inp = input('eep')
    files = resultado.get('files', [])
    id = files[0]['id']
    print(id)
    return id


def buscar_id_carpeta(nombre: str, servicio):
    resultado = servicio.files().list(q=f"name='{nombre}'",
                                      fields="nextPageToken,files(id,name, parents[], mimeType)").execute()
    files = resultado.get('files', [])
    print(files)
    id = files['parents']['id']
    return id


def obtenermime(servicio, archivo):
    print(archivo)
    resultado = servicio.files().list(q=f"name='{archivo}'").execute()
    print(resultado)
    files = resultado.get('files', [])
    mime = files[0]['mimeType']
    return mime


def actualizar_archivo_en_drive(archivo_nombre: str, servicio, ruta_archivo: str, carpeta_id_drive):
    id = buscar_id_carpeta(archivo_nombre, servicio)

    tipo_dato = mimetypes.guess_type(ruta_archivo)
    file_metadata = {
        'name': archivo_nombre,
        'mimeType': tipo_dato[0],
        'parents': [id]
    }

    contenido = MediaFileUpload(ruta_archivo, mimetype=tipo_dato[0], resumable=True)
    servicio.files().create(body=file_metadata, media_body=contenido, fields='id').execute()


def descargar_archivos(nombre_de_archivo, servicio, ruta_archivo,tipo_archivo):
    id = buscar_id_archivo(nombre_de_archivo, servicio)
    if tipo_archivo in TIPOS_A_EXPORTAR:
        tipo_exportado = TIPOS_A_EXPORTAR[tipo_archivo]
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


def listar_archivos_drive(servicio, carpetasdict, nombre_carpeta):
    lista_archivos_modificacion = {}
    id_actual = carpetasdict[nombre_carpeta]
    query = f"parents= '{id_actual}'"
    respuesta = servicio.files().list(q=query,
                                      fields="nextPageToken,files(id,name, createdTime, modifiedTime, mimeType)").execute()

    files = respuesta.get("files", [])
    print(files)
    inur = input('stop')
    for file in files:
        lista_archivos_modificacion[file['name']] = file['modifiedTime']
    return lista_archivos_modificacion


def comparar_modificaciones(direccion_carpeta: str, carpeta_id_drive: dict, servicio, lista_archivos_alumnos):
    lista_archivos = list(lista_archivos_alumnos)
    list_ruta_archivos = []
    sep = direccion_carpeta.split("\\")
    lista_archivos_local = []
    for dir in lista_archivos:
        ruta = str(dir)
        list_ruta_archivos.append(ruta)
        lista_archivos_local.append(sep[-1])

    lista_de_archivos_drive = listar_archivos_drive(servicio, carpeta_id_drive, sep[-1])
    lista_de_archivos_coincidentes = list(set(lista_archivos_local).intersection(
        set(lista_de_archivos_drive)))  # ->esta lista tiene los archivos que existen tanto en drive como en local
    lista_de_archivos_faltantes_en_drive = list(set(lista_archivos_local).difference(
        lista_de_archivos_drive))  # -> esta lista tiene los archivos que no estan en el drive
    lista_de_archivos_faltantes_en_local = list(set(lista_de_archivos_drive).difference(
        lista_archivos_local))  # -> esta lista tiene los archivos que no estan en el local

    archivos_actualizados_local = []
    archivos_actualizados_drive = []
    if len(lista_de_archivos_coincidentes) != 0:
        for archivo in lista_de_archivos_coincidentes:
            # como el archivo coincide en ambos lugares debo verificar cual fue modificado mas recientemente
            modificacion_de_archivo_local = buscar_hora_modificacion(archivo)  # ->datetime

            modificacion_de_archivo_remoto = cambiar_formato_mod_drive(archivo, servicio)  # datetime

            if modificacion_de_archivo_local > modificacion_de_archivo_remoto:
                # significa que esa carpeta en local fue modificada mas recietemente que en remota, por lo tanto esta desactualizada en drive
                actualizar_archivo_en_drive(archivo, servicio, list_ruta_archivos[list_ruta_archivos.index(archivo)],
                                            carpeta_id_drive)
                archivos_actualizados_drive.append(archivo)

            elif modificacion_de_archivo_local < modificacion_de_archivo_remoto:
                # significa que esa carpeta en remota fue modificada recientemente que en local, por lo tanto esta desactualizada en local
                descargar_archivos(sep[-1], servicio, list_ruta_archivos[list_ruta_archivos.index(archivo)])
                archivos_actualizados_local.append(archivo)

    if len(lista_de_archivos_faltantes_en_drive) != 0:
        for file in lista_de_archivos_faltantes_en_drive:
            if file not in archivos_actualizados_drive:
                actualizar_archivo_en_drive(file, servicio, list_ruta_archivos[list_ruta_archivos.index(archivo)],
                                            carpeta_id_drive)
    if len(lista_de_archivos_faltantes_en_local) != 0:
        for file in lista_de_archivos_faltantes_en_local:
            if file not in archivos_actualizados_local:
                if len(list_ruta_archivos) == 0:
                    ruta_descarga = os.path.join(direccion_carpeta, file)
                    tipo_mime=obtenermime(servicio,file)
                    descargar_archivos(file, servicio, ruta_descarga,tipo_mime)


def crear_carpeta_drive(carpeta: str, servicio):
    file_metadata = {
        'name': carpeta,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    servicio.files().create(body=file_metadata).execute()


def evaluar_carpeta(carpeta_id_drive: dict, carpeta: str, servicio):
    if carpeta not in carpeta_id_drive:
        # significa que la carpeta en local no esta en el drive
        # entonces lo creo
        crear_carpeta_drive(carpeta, servicio)
        print('la carpeta no se encontraba en drive, Carpeta creada.\n')
    else:
        lista_de_archivos_en_la_carpeta = Path(os.path.abspath(carpeta)).iterdir()
        if len(os.listdir(carpeta)) != 0:
            for docentee in lista_de_archivos_en_la_carpeta:
                print(docentee)
                if os.path.isdir(str(docentee)):
                    lista_de_archivos_docentes = Path(str(docentee)).iterdir()
                    if len(os.listdir(str(docentee))) != 0:
                        for alumno in lista_de_archivos_docentes:
                            print(alumno)
                            if os.path.isdir(str(alumno)):
                                lista_de_archivos_alumnos = Path(str(alumno)).iterdir()

                                comparar_modificaciones(str(alumno), carpeta_id_drive, servicio,
                                                        lista_de_archivos_alumnos)

                    else:
                        print(f'\ncarpeta "{docentee}" vacia')

        else:
            print(f'\ncarpeta "{carpeta}" vacia ')


def sincronizacion_remota(carpeta_id_drive: dict, servicio):
    lista_directorio_actual = os.listdir(RUTA)

    carpetas = 0
    for archivo_carpeta in lista_directorio_actual:
        if os.path.isdir(archivo_carpeta):
            carpetas += 1
            evaluar_carpeta(carpeta_id_drive, archivo_carpeta, servicio)
    else:
        if carpetas == 0:
            print('No hay carpetas , por favor crea alguna')


def main_sinc() -> None:
    carpeta_id = enlistar_carpetas_drive(SERVICIO_DRIVE)

    sincronizacion_remota(carpeta_id, SERVICIO_DRIVE)