
from apiclient import errors
import os

import service_drive
import service_gmail

import base64
import zipfile
import csv

RUTA=os.getcwd()


def generar_carpetas_local(lista_asuntos:list,opcion:int):
    try:
        carpeta=lista_asuntos[(opcion)-1]

        directorio_nuevo=os.path.join(RUTA,carpeta)

        os.makedirs(directorio_nuevo)
    except OSError:
        print('Error en el nombre de la ruta, Vuelva a seleccionar el mensaje')



def buscar_asunto():
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
    nombre, extension= os.path.splitext(archivo)
    if extension!='.zip':
        print(f'El archivo {nombre} no es un un archivo zip')
    else:
        archivozip= zipfile.ZipFile(archivo)
        archivozip.extractall()
        archivozip.close()


def enlistar_doc_alum()->list:
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








def buscar_emails(servicio)->list:
    lista_final=[]
    emails= servicio.users().messages().list(userId='me',maxResults=5).execute()
    mensajes= emails['messages']
    for ids in mensajes:
        lista_final.append(ids['id'])
    return lista_final

def mostrar_emails(servicio, lista_ids:list):
    lista_asuntos=[]
    for i in lista_ids:
        msjes= servicio.users().messages().get(userId='me',id=i,format='full').execute()
        cabezales=msjes['payload']['headers']

        for i in cabezales:
            if i['name']=='Subject':
                lista_asuntos.append(i['value'])
    return lista_asuntos

def seleccionar_email(lista_asuntos:list, servicio):
    print('A continuacion se muestra los ultimos 5 mails recibidos con sus asuntos: \n')
    for i in range(5):
        print(f'{i+1}) {lista_asuntos[i]}')
    opcion = input('Por favor elige cual crees que sea el mensaje, si no aparece presiona 0 para actualizar: ')
    while not opcion.isnumeric():
        opcion=input('Ingrese un numero o 0 para actualizar: ')
    while opcion=='0':
        lista_ids=buscar_emails(servicio)
        lista_asuntos=mostrar_emails(servicio,lista_ids)
        print('A continuacion se muestra los ultimos 5 mails recibidos con sus asuntos: \n')
        for i in range(5):
            print(f'{i + 1}) {lista_asuntos[i]}')
        opcion = input('Por favor elige cual crees que sea el mensaje, si no aparece presiona 0 para actualizar: ')

    else:
        return int(opcion)


def opciones()->int:
    print('1)Generar carpetas localmente')
    print('2)Generar carpetas en Google Drive')
    opcion=input('\nIngrese una opcion: ')
    while not opcion.isnumeric():
        opcion=input('\nError, Vuelva a ingresar: ')
    return int(opcion)

def anidar_carpetas(lista_asuntos, opcion, lista_csv):
    carpeta_de_parcial= lista_asuntos[(opcion) - 1]
    direccion_evaluacion= os.path.join(RUTA,carpeta_de_parcial)
    lista_alumnos=lista_csv[0]
    lista_docentes=lista_csv[1]
    doc_alumno=lista_csv[2]
    print(doc_alumno)
    print(type(doc_alumno))
    lista_paths=[]
    '''for docente in lista_docentes:
        dir=os.path.join(direccion_evaluacion, docente)
        os.mkdir(dir)'''

    for docente in doc_alumno:
        for lista in range(len(doc_alumno[docente])):
            direccion1= os.path.join(direccion_evaluacion,docente)

            direccion2=os.path.join(direccion1,doc_alumno[docente][lista])
            os.makedirs(direccion2)







def main_carpetas()->None:

    servicio_gmail = service_gmail.obtener_servicio()
    servicio_drive= service_drive.obtener_servicio()

    opcion = opciones()

    if opcion == 1:
        lista_idmsjes = buscar_emails(servicio_gmail) #busca los ultimos 5 mensajes

        lista_asuntos = mostrar_emails(servicio_gmail, lista_idmsjes) #muestra los ultimos 5 mensajes por Asunto

        opcion = seleccionar_email(lista_asuntos, servicio_gmail) #el usuario elije cual mensaje

        generar_carpetas_local(lista_asuntos,opcion) #genera las carpetas localmente con el asunto del mail elegido

        nombre_archivo= descargar_archivo(servicio_gmail,lista_idmsjes,opcion) #descarga el archivo adjunto

        descomprimir_zip(nombre_archivo)

        listas_csv=enlistar_doc_alum()

        anidar_carpetas(lista_asuntos,opcion,listas_csv)

    elif opcion==2:
        pass



main_carpetas()
