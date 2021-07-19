import os
import time
import service_drive
import service_gmail
import datetime
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io
RUTA= os.getcwd()

SERIVICO_GMAIL= service_gmail.obtener_servicio()

SERVICIO_DRIVE= service_drive.obtener_servicio()

def enlistar_carpetas_drive(servicio_drive)->dict:
    nombre_carpeta_modificacion = {} # {nombre:fecha_de_modificacion}

    resultado= servicio_drive.files().list(q="mimeType= 'application/vnd.google-apps.folder' and 'me' in owners and trashed=false",
                                           fields="nextPageToken,files(id,name, createdTime, modifiedTime, mimeType)").execute()

    datos= resultado.get('files',[])
    for i in datos:
        print(i)
        nombre_carpeta_modificacion[i['name']]= i['modifiedTime']
    return nombre_carpeta_modificacion

def buscar_hora_modificacion(carpeta:str):
    estado=os.stat(carpeta).st_mtime
    fecha= time.localtime(estado)
    fecha= datetime.datetime(fecha[0],fecha[1],fecha[2],fecha[3],fecha[4],fecha[5])
    return fecha

def cambiar_formato_mod_drive(horario_modificacion_carpeta:str):
    dt=datetime.datetime.strptime(horario_modificacion_carpeta,"%Y-%m-%dT%H:%M:%S.%fZ")#->datetime
    cambio_formato=dt.strftime("%Y-%m-%d%H:%M:%S")#->str
    final=datetime.datetime.strptime(cambio_formato,"%Y-%m-%d%H:%M:%S")#->datetime

    return final

def buscar_id_archivo(nombre_archivo,servicio):
    mime = obtenermime(servicio,nombre_archivo)
    resultado= servicio.files().list(q=f"name='{nombre_archivo}', mimeType= '{mime}'").execute()
    files= resultado.get('files',[])
    id= files.get('id')
    return id




def buscar_id_carpeta(nombre:str,servicio):
    resultado=servicio.files().list(q=f"name='{nombre}',mimeType= 'application/vnd.google-apps.folder'").execute()
    files= resultado.get('files',[])
    id=files.get('id')
    return id

def obtenermime(servicio, archivo):
    resultado = servicio.files().list(q=f"name='{archivo}'").execute()
    files = resultado.get('files', [])
    mime = files.get('mimeType')
    return mime

def actualizar_carpeta_en_drive(carpeta_nombre:str,servicio,lista_archivos:list):
    id=buscar_id_carpeta(carpeta_nombre,servicio)
    for archivo in lista_archivos:
        file_metadata={
            'name':archivo,
            'parents':[id]
        }
        tipo_dato=obtenermime(servicio,archivo)
        contenido= MediaFileUpload(archivo,mimetype=tipo_dato)
        servicio.files().create(body=file_metadata, media_body=contenido,fields='id').execute()






def descargar_archivos(ruta,servicio,lista_de_archivos):
    lista_ids=[]
    for archivo in lista_de_archivos:
        id= buscar_id_archivo(archivo,servicio)
        lista_ids.append(id)
        resultado= servicio.files().get_media(fileId= id).execute()
        fh= io.BytesIO
        descarga= MediaIoBaseDownload(fd= fh, request= resultado)

        completado= False
        while not completado:
            estado, completado = descarga.next_chunk()
            print(f'descargando... {estado.progress()*100}')
        fh.seek(0)
        direccion=os.path.join(ruta,archivo)
        with open(direccion,'wb')as file:
            file.write(fh.read())



def comparar_modificaciones(carpeta:str,carpeta_modificaciones:dict,servicio,lista_archivos_alumnos:list):
    modificacion_de_carpeta_local= buscar_hora_modificacion(carpeta)#->datetime
    modificacion_de_carpeta_remota= cambiar_formato_mod_drive(carpeta_modificaciones[carpeta])#datetime
    if modificacion_de_carpeta_local > modificacion_de_carpeta_remota:
        #significa que esa carpeta en local fue modificada mas recietemente que en remota, por lo tanto esta desactualizada en drive
        actualizar_carpeta_en_drive(carpeta,servicio,lista_archivos_alumnos)
    else:
        # significa que esa carpeta en local fue modificada mas antes que en remota, por lo tanto esta desactualizada en local
        ruta_carpeta=os.path.abspath(carpeta)
        descargar_archivos(ruta_carpeta,servicio,lista_archivos_alumnos)



def crear_carpeta_drive(carpeta:str,servicio):
    file_metadata={
        'name': carpeta,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    servicio.files().create(body=file_metadata).execute()



def evaluar_carpeta(carpeta_modificacion_drive:dict,carpeta:str,servicio):
    if carpeta not in carpeta_modificacion_drive:
        # significa que la carpeta en local no esta en el drive
        # entonces lo creo
        crear_carpeta_drive(carpeta, servicio)
    else:
        lista_de_archivos_en_la_carpeta=os.scandir(carpeta)
        for docente in lista_de_archivos_en_la_carpeta:
            if os.path.isdir(docente):
                lista_de_archivos_docentes=os.scandir(docente)
                for alumno in lista_de_archivos_docentes:
                    if os.path.isdir(alumno):
                        lista_de_archivos_alumnos=os.scandir(alumno)
                        comparar_modificaciones(carpeta,carpeta_modificacion_drive,servicio,lista_de_archivos_alumnos)



def sincronizacion_remota(carpeta_modificacion_drive:dict,servicio):

    lista_directorio_actual=os.listdir(RUTA)
    print(lista_directorio_actual)
    for archivo_carpeta in lista_directorio_actual:
        if os.path.isdir(archivo_carpeta):
            evaluar_carpeta(carpeta_modificacion_drive,archivo_carpeta,servicio)
            lista_de_la_carpeta=os.scandir(archivo_carpeta)
            for i in lista_de_la_carpeta:
                if os.path.isdir(i):
                    evaluar_carpeta(carpeta_modificacion_drive,i,servicio)






def main_sinc()->None:

    carpeta_modificacion = enlistar_carpetas_drive(SERVICIO_DRIVE)

    sincronizacion_remota(carpeta_modificacion,SERVICIO_DRIVE)