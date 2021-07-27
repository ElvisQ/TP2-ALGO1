import os, time
import pandas as pd
from auxiliar import SERV_DR, RUTA

ESPACIOS = '''\n¿Dónde desea buscar?\n
1. Archivos en carpeta local.
2. Archivos en carpeta remota.
'''

def validar_entrada(entrada: any, limite_inf: int, limite_sup: int) -> int:
    '''
    PRE: Recibe una entrada y dos límites en los cuales debe estar contenida la entrada
    POST: Verifica que sea numérico y que esté dentro de los límites especificados, caso contrario le pide al usuario volver a ingresar hasta que se cumpla la condición. Si todo es correcto, se devuelve la entrada como int.
    '''
    while not entrada.isnumeric():
        entrada = input("Entrada no válida. Debe ingresar un número: ")
    entrada = int(entrada)
    while entrada <= limite_inf or entrada >= limite_sup+1:
        entrada = input("No existe esa opción. Ingrese otro índice: ")
        while not entrada.isnumeric():
             entrada = input("Entrada no válida. Debe ingresar un número: ")
             entrada = int(entrada)
    return entrada

def listar_subcarpeta_local(subcarpetas: list, ruta_actual: str) -> None:
    '''
    PRE: Recibe al directorio actual y a una lista de subcarpetas contenidas en él.
    POST: Lista la subcarpeta local que eligió el usuario.
    '''
    sublistado = input("¿Qué carpeta desea abrir? ")
    indice = validar_entrada(sublistado,0,len(subcarpetas))
    nueva_ruta = os.path.join(ruta_actual,subcarpetas[indice-1])
    listar_local(nueva_ruta)

def abrir_subcarpeta() -> str:
    '''
    POST: Pide al usuario una respuesta de sí/no y verifica que sea válida. Si es así, la devuelve.
    '''
    respuesta = input("\n¿Desea abrir alguna carpeta? (s/n) ")
    while respuesta != "s" and respuesta != "n":
        respuesta = input("Entrada no válida. ¿Abrir carpeta? (s/n) ")
    return respuesta

def navegar_subcarpeta_local(contenido_directorio: list, ruta_actual: str) -> None:
    '''
    PRE: Recibe el directorio actual y su contenido.
    POST: Muestra por pantalla las subcarpetas que están contenidas en la carpeta actual. Pregunta al usuario si quiere ver el contenido de las mismas.
    '''
    subcarpetas = []
    for i in range(len(contenido_directorio)):
        ruta_subcarpeta = os.path.join(ruta_actual,contenido_directorio[i])
        if os.path.isdir(ruta_subcarpeta):
            subcarpetas.append(contenido_directorio[i])
    if len(subcarpetas) != 0:
        print("\nSubcarpetas en",ruta_actual,"\n")
        for j in range(len(subcarpetas)):
            print(j+1,subcarpetas[j])
        respuesta = abrir_subcarpeta()
        if respuesta == "s":
            listar_subcarpeta_local(subcarpetas,ruta_actual)

def listar_local(rutap: str) -> None:
    '''
    PRE: Recibe una ruta del entorno local del usuario
    POST: Lista los archivos del directorio. Luego procede con las subcarpetas
    '''
    contenido = os.listdir(rutap)  
    ult_modif = []
    extensiones = []
    nombres = []
    for i in range(len(contenido)):
        ruta_archivo = os.path.join(rutap,contenido[i])
        ult_modif.append(time.ctime(os.path.getmtime(ruta_archivo)))
        ext_individuales = contenido[i].split('.')
        if len(ext_individuales) == 1:
            ext_individuales.append('(carpeta)')
        extensiones.append(ext_individuales[1])
        nombres.append(ext_individuales[0])
    datos = {'Nombre':nombres,'Extensión':extensiones,'Última modificación':ult_modif}
    listado_pantalla = pd.DataFrame(datos)
    print("\nContenido de",rutap,"\n")
    print(listado_pantalla)
    navegar_subcarpeta_local(contenido,rutap)
    
def modificar_fecha(fecha: str) -> str:
    '''
    PRE: Recibe las fechas de última modificación de los archivos remotos.
    POST: Modifica el formato y lo devuelve.
    '''
    lista = fecha.split('-')
    fecha2 = lista[2]
    lista2 = fecha2.split('T')
    fecha3 = lista2[1]
    lista3 = fecha3.split('.')
    listadef = [lista2[0],lista[1],lista[0]]
    fechadef = "-".join(listadef)
    return fechadef + " " + lista3[0]

def listar_subcarpeta_remota(subcarpetas: list) -> None:
    '''
    PRE: Si el usuario especificó que sí quería listar una subcarpeta, esta función recibe una lista con las subcarpetas contenidas en la carpeta listada última. 
    POST: Pregunta al usuario cuál quiere listar. Luego reinicia el proceso de listado pero dentro de esa subcarpeta.
    '''
    indice = input("¿Qué carpeta desea abrir? ")
    indicec = validar_entrada(indice,0,len(subcarpetas))
    carpeta = subcarpetas[indicec-1]['id']
    listar_remoto(carpeta)

def mostrar_subcarpetas_remota(archivos: list) -> None:
    '''
    PRE: Recibe los archivos que se recopilaron en el último listado.
    POST: Busca y muestra las subcarpetas contenidas en la carpeta correspondiente de Drive. Luego pregunta si quiere listar alguna de las subcarpetas.
    '''
    subcarpetas_r = []
    for i in range(len(archivos)):
        tipo_arch = str(archivos[i]['mimeType'])
        es_carpeta = tipo_arch.endswith('.folder')
        if es_carpeta:
            subcarpetas_r.append(archivos[i])
    if len(subcarpetas_r) != 0:
        print("\nSubcarpetas en directorio actual:\n")
        for car in range(len(subcarpetas_r)):
            print(car+1,subcarpetas_r[car]['name'])
        respuesta = abrir_subcarpeta()
        if respuesta == "s":
            listar_subcarpeta_remota(subcarpetas_r)

def proceso_remoto_nativo(servicio: any) -> list:
    '''
    PRE: Recibe el service de Drive para las funciones específicas.
    POST: Recopila los archivos de la unidad de Drive del usuario y los devuelve en una lista.
    '''
    lista_remota = servicio.files().list(fields='nextPageToken, files(id, name, mimeType, modifiedTime, parents)').execute()
    archivos = lista_remota.get('files')
    nextPageToken = lista_remota.get('nextPageToken')
    while nextPageToken:
        lista_remota = servicio.files().list(fields='nextPageToken, files(id, name, mimeType, modifiedTime, parents)',pageToken=nextPageToken).execute()
        archivos.extend(lista_remota.get('files'))
        nextPageToken = lista_remota.get('nextPageToken')
    return archivos

def proceso_remoto_custom(servicio: any, carpeta: str) -> list:
    '''
    PRE: Recibe el service de Drive para las funciones específicas y la carpeta que el usuario quiere listar.
    POST: Recopila los archivos de la carpeta del Drive elegida por el usuario y los devuelve en una lista.
    '''
    query = f"parents = '{carpeta}'"
    lista_remota = servicio.files().list(q=query,fields='nextPageToken, files(id, name, mimeType, modifiedTime, parents)').execute()
    archivos = lista_remota.get('files')
    nextPageToken = lista_remota.get('nextPageToken')
    while nextPageToken:
        lista_remota = servicio.files().list(q=query,fields='nextPageToken, files(id, name, mimeType, modifiedTime, parents)',pageToken=nextPageToken).execute()
        archivos.extend(lista_remota.get('files'))
        nextPageToken = lista_remota.get('nextPageToken')
    return archivos

def listar_remoto(carpeta: any) -> None:
    '''
    PRE: Recibe una carpta de Drive que el usuario quiere listar. Por default es 0.
    POST: Lista los archivos de la carpeta del usario y da la opción de listar subcarpetas. La carpeta default ("0") es el MyDrive del usuario.
    '''
    if isinstance(carpeta,int):
        archivos = proceso_remoto_nativo(SERV_DR)
    else:
        archivos = proceso_remoto_custom(SERV_DR,carpeta)
    nombres_d = []
    tipo_d = []
    ult_modif_d = []
    for i in range(len(archivos)):
        ult_modif_d.append(modificar_fecha(archivos[i]['modifiedTime']))
        tipo_d.append(archivos[i]['mimeType'])
        nombres_d.append(archivos[i]['name'])
    datos = {'Nombre':nombres_d,'Tipo':tipo_d,'Últ. modif. (día/hora)':ult_modif_d}
    listado_pantalla_d = pd.DataFrame(datos)
    print(listado_pantalla_d)
    mostrar_subcarpetas_remota(archivos)

def ejecutar_listado(espacio: int) -> None:
    '''
    PRE: Recibe el espacio ("local" o "remoto") como opción numérica que eligió el usuario.
    POST: ejecuta las funciones que listan el contenido del espacio elegido.
    '''
    print("Recopilando...")
    if espacio == 1:
        listar_local(RUTA)
    elif espacio == 2:
        carpeta = 0
        listar_remoto(carpeta)
    else:
        print("Esa opcion no existe")
        espacio_elegido = elegir_espacio() 
        ejecutar_listado(espacio_elegido)

def main_listado() -> None:
    print(ESPACIOS)
    espacio_elegido = input()
    espacio_elegido = validar_entrada(espacio_elegido,0,2)
    ejecutar_listado(espacio_elegido)

