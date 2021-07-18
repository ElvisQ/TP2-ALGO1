import os, time, service_drive
from typing import Any
import pandas as pd

ESPACIOS = '''\n¿Dónde desea buscar?\n
1. Archivos en carpeta local.
2. Archivos en carpeta remota.
'''
RUTA_TRABAJO = os.getcwd()

def validar_entero(entrada: str) -> int:
    '''
    Recibe un string. Si es numérico lo devuelve como integer, caso contrario le pide al usuario volver a ingresar.
    '''    
    while not entrada.isnumeric():
        entrada = input("Entrada no válida. Debe ingresar un número: ")
    return int(entrada)

def validar_subcarpeta(indice: int, cantidad_subcarpetas: int) -> int:
    '''
    Recibe el índice de subcarpeta elegido. Si no existe, pide al usuario reingresarlo.
    '''
    while indice <= 0 or indice >= cantidad_subcarpetas+1:
        indice = input("No existe esa carpeta. Ingrese otro índice: ")
        indice = validar_entero(indice)
    return int(indice)

def elegir_espacio() -> int:
    '''
    Printea las opciones y pide al usuario que elija una. Luego, la devuelve.
    '''
    print(ESPACIOS)
    espacio_elegido = input("Elija una opcion: ")
    while not espacio_elegido.isnumeric():
        espacio_elegido = input("Debe ingresar un numero. Elija una opcion: ")
    return int(espacio_elegido)

def listar_subcarpeta_local(subcarpetas: list, ruta_actual: str) -> None:
    '''
    Lista la subcarpeta local que eligió el usuario.
    '''
    sublistado = input("¿Qué carpeta desea abrir? ")
    sublistado_num = validar_entero(sublistado)
    indice = validar_subcarpeta(sublistado_num,len(subcarpetas))
    nueva_ruta = os.path.join(ruta_actual,subcarpetas[indice-1])
    listar_local(nueva_ruta)
    
def navegar_subcarpeta_local(contenido_directorio: list, ruta_actual: str) -> None:
    '''
    Muestra por pantalla las subcarpetas que están contenidas en la carpeta actual. Pregunta al usuario si quiere ver el contenido de las mismas.
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
        respuesta = input("\n¿Desea abrir alguna carpeta? (s/n) ")
        while respuesta != "s" and respuesta != "n":
            respuesta = input("Entrada no válida. ¿Abrir carpeta? (s/n) ")
        if respuesta == "s":
            listar_subcarpeta_local(subcarpetas,ruta_actual)
   
def listar_local(rutap: str) -> None:
    '''
    Lista los archivos de la carpeta local actual.
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
    Modifica el formato de la fecha de última modificación de un archivo de Drive.
    '''
    lista = fecha.split('-')
    fecha2 = lista[2]
    lista2 = fecha2.split('T')
    fecha3 = lista2[1]
    lista3 = fecha3.split('.')
    listadef = [lista2[0],lista[1],lista[0]]
    fechadef = "-".join(listadef)
    return fechadef + " " + lista3[0]

def listar_subcarpeta_remota(subcarpetas: list):
    '''
    Lista la subcarpeta remota que eligió el usuario.
    '''
    indice = input("¿Qué carpeta desea abrir? ")
    indicec = validar_entero(indice)
    indicev = validar_subcarpeta(indicec,len(subcarpetas))
    carpeta = subcarpetas[indicev-1]['id']
    listar_remoto(carpeta)


def mostrar_subcarpetas_remota(archivos: list):
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
        respuesta = input("\n¿Desea abrir alguna carpeta? (s/n) ")
        while respuesta != "s" and respuesta != "n":
            respuesta = input("Entrada no válida. ¿Abrir carpeta? (s/n) ")
        if respuesta == "s":
            listar_subcarpeta_remota(subcarpetas_r)

def listar_remoto(carpeta) -> None:
    '''
    Lista los archivos de la carpeta remota actual.
    '''
    servicio = service_drive.obtener_servicio()
    if isinstance(carpeta,int):
        lista_remota = servicio.files().list(fields='files(id,mimeType,name,modifiedTime,parents)').execute()
    else:
        query = f"parents = '{carpeta}'"
        lista_remota = servicio.files().list(q=query,fields='files(id,mimeType,name,modifiedTime,parents)').execute()
    archivos = lista_remota['files']
    pd.set_option('max_rows',len(archivos))
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
    Recibe una opcion numerica y ejecuta una funcion segun lo elegido.
    '''
    if espacio == 1:
        listar_local(RUTA_TRABAJO)
    elif espacio == 2:
        carpeta = 0
        listar_remoto(carpeta)
    else:
        print("Esa opcion no existe")
        espacio_elegido = elegir_espacio() 
        ejecutar_listado(espacio_elegido)

def main_listado() -> None:
    espacio_elegido = elegir_espacio()
    ejecutar_listado(espacio_elegido)
