import os
import service_gmail


RUTA=os.getcwd()


'''servicio=service_gmail.obtener_servicio()
resultados= servicio.users().messages().list(userId='me',labelIds = ['INBOX']).execute()
mensajes=resultados.get('messages', [])
if not mensajes:
    print("No messages found.")
else:
    print("Message snippets:")
    for message in mensajes:
        msg = servicio.users().messages().get(userId='me', id=message['id']).execute()
        print(msg['snippet'])
'''
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
    if opcion=='0':
        lista_ids=buscar_emails(servicio)
        lista_asuntos=mostrar_emails(servicio,lista_ids)
        seleccionar_email(lista_asuntos,servicio)
    else:
        return int(opcion)


def opciones()->int:
    print('1)Generar carpetas localmente')
    print('2)Generar carpetas en Google Drive')
    opcion=input('\nIngrese una opcion: ')
    while not opcion.isnumeric():
        opcion=input('\nError, Vuelva a ingresar: ')
    return int(opcion)



def main_carpetas()->None:
    servicio= service_gmail.obtener_servicio()
    opcion=opciones()
    if opcion==1:
        lista_idmsjes = buscar_emails(servicio)
        lista_asuntos = mostrar_emails(servicio, lista_idmsjes)
        opcion = seleccionar_email(lista_asuntos, servicio)
        generar_carpetas_local(lista_asuntos,opcion)
    elif opcion==2:
        pass

main_carpetas()
