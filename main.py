import opciones

MENU = '''\nElija una de las siguientes opciones:\n
1. Listar archivos de la carpeta actual.
2. Crear un archivo.
3. Subir un archivo.
4. Descargar un archivo.
5. Sincronizar carpetas y archivos.
6. Generar carpetas de una evaluacion.
7. Actualizar entregas de alumnos via mail.
8. Salir.
'''

def main():

    salida = False
    while not salida:
        print(MENU)
        opcion = opciones.validar_opcion()
        salida = opciones.ejecutar_opcion(opcion,salida)

main()

