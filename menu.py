
import service_drive
import service_gmail
import listado
import carpetasgen
import sincronizar

MENU = '''Elija una de las siguientes opciones:
1. Listar archivos de la carpeta actual.
2. Crear un archivo.
3. Subir un archivo.
4. Descargar un archivo.
5. Sincronizar carpetas y archivos.
6. Generar carpetas de una evaluacion.
7. Actualizar entregas de alumnos via mail.
8. Salir.
'''

DRIVE_SERVICE= service_drive.obtener_servicio()
GMAIL_SERVICE= service_gmail.obtener_servicio()

def validar_opcion() -> int:
#Pide el ingreso de una opcion y verifica que sea numerica.
    opcion = input('\nIngrese una opcion: ')
    while not opcion.isnumeric():
        opcion = input("Entrada no valida. Debe ingresar un numero: ")
    return int(opcion)

def ejecutar_opcion(opcion: int, salida: bool) -> bool:
#Recibe una opcion numerica y ejecuta una funcion segun lo elegido.
    if opcion == 1:
        listado.main_listado()
    elif opcion == 2:
        pass
    elif opcion == 3:
        pass
    elif opcion == 4:
        pass
    elif opcion == 5:
        sincronizar.main_sinc()
    elif opcion == 6:
        carpetasgen.main_carpetas()
    elif opcion == 7:
        pass
    elif opcion == 8:
        salida = True
    else:
        print("Esa opcion no existe. Reingrese opcion: ")
        opcion = validar_opcion()
        ejecutar_opcion(opcion,salida)
    return salida

def main():

    salida = False
    while not salida:
        print(MENU)
        opcion = validar_opcion()
        salida = ejecutar_opcion(opcion,salida)

main()
