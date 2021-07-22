
from apiclient import errors
import os

import service_drive
import service_gmail

import base64
import zipfile
import csv

RUTA=os.getcwd()

SERVICIO_GMAIL = service_gmail.obtener_servicio()
SERVICIO_DRIVE = service_drive.obtener_servicio()

def generar_carpetas_local(lista_asuntos:list,opcion:int):
    '''
    PRE:Recibe la lista de asuntos junto con la opcion elegida por el usuario
    POST: Crea las carpetas de los parciales localmente
    '''
    try:
        print('\n Creando carpetas...\n')
        carpeta=lista_asuntos[(opcion)-1]

        directorio_nuevo=os.path.join(RUTA,carpeta)

        os.makedirs(directorio_nuevo)
        return False
    except OSError:
        print('Error en el nombre de la ruta, Vuelva a seleccionar el mensaje')
        return True




def buscar_asunto():
    '''
    Busca los asuntos de los emails
    '''
    servicio= service_gmail.obtener_servicio()
    resultados = servicio.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    mensajes= resultados.get('messages',[])

    for mensaje in mensajes:
        msg=servicio.users().messages().get(userId='me', id= mensaje['id']).execute()


    headers = msg["payload"]["headers"]
    for i in headers:
        nameindict = i["name"]
        if nameindict == "Subject":
            print(i["value"])
        if nameindict == "Date":
            print(i["value"])


def descargar_archivo(servicio, idmsjes:list,opcion:int)->str:
    '''
    PRE:Recibe el servicio de gmail con una lista de ids de mensajes junto con la opcion elegida por el usuario
    POST:Descarga el archivo y retorna su nombre
    '''
    try:
        nombre_archivo=''
        id_elegido=idmsjes[(opcion) - 1]
        mensaje=servicio.users().messages().get(userId='me',id=id_elegido,).execute()
        partes= mensaje['payload']['parts']         #lista de partes de un mensaje

        for parte in partes:
            if parte['filename']:
                if 'data' in parte['body']:
                    data= partes['body']['data']
                else:
                    adjuntoid=parte['body']['attachmentId']
                    adjunto=servicio.users().messages().attachments().get(userId='me',messageId=id_elegido, id=adjuntoid).execute()
                    data=adjunto['data']
                nombre_archivo= parte['filename']
                datos_de_archivo= base64.urlsafe_b64decode(data.encode('UTF-8'))

                with open(nombre_archivo,'wb') as archivo:
                    archivo.write(datos_de_archivo)
        return nombre_archivo

    except errors.HttpError:
        print('Ocurrio un error vuelve a intentarlo')



def descomprimir_zip(archivo:str):
    '''
    PRE:Recibe el nombre del archivo a descomprimir
    POST: Descomprime el archivo
    '''
    nombre, extension= os.path.splitext(archivo)
    if extension!='.zip':
        print(f'El archivo {nombre} no es un un archivo zip')
        return False
    else:
        archivozip= zipfile.ZipFile(archivo)
        archivozip.extractall()
        archivozip.close()
        return True


def enlistar_doc_alum()->list:
    '''
    Se genera un diccionario con el docente como clave y una lista con los alumnos correspondietes como valor
    todo esto a partir del archivo.zip enviado. Retorna una lista con listas de docentes, alumnos y relacion docente-alumno
    '''
    lista_docentes=[]
    lista_alumnos=[]
    dic_doc_alum={} #key:docente, value:[alumno correspondiente]
    lista_total=[]
    try:
        with open('alumnos.csv',mode='r',newline='',encoding='UTF-8') as alumnos:
            lector_csva= csv.reader(alumnos,delimiter=',')
            next(lector_csva)
            for fila in lector_csva:
                lista_alumnos.append(fila[0])
            lista_total.append(lista_alumnos)
        with open('docentes.csv',mode='r',newline='',encoding='UTF-8') as docentes:
            lector_csvd= csv.reader(docentes, delimiter=',')
            next(lector_csvd)
            for fila in lector_csvd:
                lista_docentes.append(fila[0])
            lista_total.append(lista_docentes)
        with open('docente-alumnos.csv',mode='r',newline='',encoding='UTF-8') as doc_alum:
            csv_reader=csv.reader(doc_alum,delimiter=',')
            next(csv_reader)
            for fila in csv_reader:
                if fila[0] not in dic_doc_alum:
                    dic_doc_alum[fila[0]]=[]
                    dic_doc_alum[fila[0]].append(fila[1])
                else:
                    dic_doc_alum[fila[0]].append(fila[1])
            lista_total.append(dic_doc_alum)

        return lista_total

    except IOError:
        print('Falta un archivo o revisa bien el nombre del archivo')
        main_carpetas()



def buscar_emails(servicio)->list:
    '''
    PRE: Recibe el servicio de gmail
    POST: Retorna una lista con los id de los primeros 5 mensajes
    '''
    lista_final=[]
    emails= servicio.users().messages().list(userId='me',maxResults=5).execute()
    mensajes= emails['messages']
    for ids in mensajes:
        lista_final.append(ids['id'])
    print('\nBuscando emails...\n')
    return lista_final


def adjuntar_emails(servicio, lista_ids:list):
    '''
    PRE: Recibe el servicio de gmail y la lista de ids de cadad mensaje
    POST: Retorna una lista con los asuntos de esos mensajes
    '''
    lista_asuntos=[]
    for i in lista_ids:
        msjes= servicio.users().messages().get(userId='me',id=i,format='full').execute()
        cabezales=msjes['payload']['headers']

        for i in cabezales:
            if i['name']=='Subject':
                lista_asuntos.append(i['value'])
    return lista_asuntos


def seleccionar_email(lista_asuntos:list, servicio):
    '''
    PRE: Recibe una lista de asuntos de mensajes y el servicio de gmail
    POST: Muestra los mensajes y Retorna la opcion elegida por el usuario
    '''
    print('A continuacion se muestra los ultimos 5 mails recibidos con sus asuntos: \n')
    for i in range(5):
        print(f'{i+1}) {lista_asuntos[i]}')
    opcion = input('Por favor elige cual crees que sea el mensaje, si no aparece presiona 0 para actualizar: ')
    while not opcion.isnumeric():
        opcion=input('Ingrese un numero o 0 para actualizar: ')
    while opcion=='0':
        lista_ids=buscar_emails(servicio)
        lista_asuntos=adjuntar_emails(servicio,lista_ids)
        print('A continuacion se muestra los ultimos 5 mails recibidos con sus asuntos: \n')
        for i in range(5):
            print(f'{i + 1}) {lista_asuntos[i]}')
        opcion = input('Por favor elige cual crees que sea el mensaje, si no aparece presiona 0 para actualizar: ')

    else:
        return int(opcion)



def anidar_carpetas(lista_asuntos, opcion, lista_csv):
    '''
    PRE: Recibe la lista de asuntos con la opcion que eligio el usuario y la lista con las listas de relacion docente-alumno
    POST: Genera las carpetas anidadas localmente
    '''
    carpeta_de_parcial= lista_asuntos[(opcion) - 1]
    direccion_evaluacion= os.path.join(RUTA,carpeta_de_parcial)
    doc_alumno=lista_csv[2]

    for docente in doc_alumno:
        for lista in range(len(doc_alumno[docente])):
            direccion1= os.path.join(direccion_evaluacion,docente)

            direccion2=os.path.join(direccion1,doc_alumno[docente][lista])
            os.makedirs(direccion2)


def crear_carpetas_drive(servicio_drive, lista_asuntos:list, opciondenombre:int ,listas_csv:list):
    '''
    PRE: Recibe el servicio de gmail la lista de asuntos con la opcion elegida y la listas relacion docente-alumno
    POST: Crea las carpetas anidadas en el Drive
    '''
    print('\nCreando carpetas en Google Drive...\n')
    docente_alumno=listas_csv[2] #docente:[alumnos]

    nombre_carpeta= lista_asuntos[(opciondenombre)-1]

    file_metadata = {
        'name': nombre_carpeta,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = servicio_drive.files().create(body=file_metadata, fields='id').execute()
    id_carpeta_examen=file.get('id')
    lista_idscarp_docentes= {} #{idcarpetadoc: [alumnos_correspondientes]}
    for docente in docente_alumno:

        file_metadata={
            'name':docente,
            'mimeType':'application/vnd.google-apps.folder',
            'parents': [id_carpeta_examen]
        }
        carpeta=servicio_drive.files().create(body=file_metadata).execute()
        id_carpeta_doc=carpeta.get('id')

        for i in range(len(docente_alumno[docente])):
            if id_carpeta_doc not in lista_idscarp_docentes:
                lista_idscarp_docentes[id_carpeta_doc]=[]
                lista_idscarp_docentes[id_carpeta_doc].append(docente_alumno[docente][i])
            else:
                lista_idscarp_docentes[id_carpeta_doc].append(docente_alumno[docente][i])

    for id_carpeta in lista_idscarp_docentes:
        alumnos=lista_idscarp_docentes[id_carpeta]
        for i in range(len(alumnos)):
            file_metadata={
                'name': alumnos[i],
                'mimeType':'application/vnd.google-apps.folder',
                'parents': [id_carpeta]
            }
            servicio_drive.files().create(body=file_metadata).execute()
    print("Carpetas creadas, actualize la pagina.")



def main_carpetas()->None:
    error= False

    while not error:
        lista_idmsjes = buscar_emails(SERVICIO_GMAIL) #busca los ultimos 5 mensajes

        lista_asuntos = adjuntar_emails(SERVICIO_GMAIL, lista_idmsjes) #adjunta los ultimos 5 mensajes por Asunto en una lista

        opcion = seleccionar_email(lista_asuntos, SERVICIO_GMAIL) #el usuario elije cual mensaje

        rompio =generar_carpetas_local(lista_asuntos,opcion) #genera las carpetas localmente con el asunto del mail elegido
        if rompio==False:

            nombre_archivo= descargar_archivo(SERVICIO_GMAIL, lista_idmsjes, opcion) #descarga el archivo adjunto

            descomprimir=descomprimir_zip(nombre_archivo) #descomprime el archivo .zip
            if descomprimir==True:
                listas_csv=enlistar_doc_alum() #enlista la relacion docente alumno segun losr archivos csv

                anidar_carpetas(lista_asuntos,opcion,listas_csv) #anida las carpetas localmente

                crear_carpetas_drive(SERVICIO_DRIVE, lista_asuntos, opcion, listas_csv) #crea y anida las carpetas en el drive

                error= True
