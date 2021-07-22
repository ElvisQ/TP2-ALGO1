import listado, crear_archivo, subir_archivo

def validar_opcion() -> int:
#Pide el ingreso de una opcion y verifica que sea numerica.   
    opcion = input()
    while not opcion.isnumeric():
        opcion = input("Entrada no valida. Debe ingresar un numero: ")
    return int(opcion)

def ejecutar_opcion(opcion: int, salida: bool) -> bool:
#Recibe una opcion numerica y ejecuta una funcion segun lo elegido.
    if opcion == 1:
        listado.main_listado()
    elif opcion == 2:
        crear_archivo.crear()
    elif opcion == 3:
        subir_archivo.archivo_subido()
    elif opcion == 4:
        descargar_archivos()
    elif opcion == 5:
        sincronizar()
    elif opcion == 6:
        generar_carpetas()
    elif opcion == 7:
        actualizar_entregas()
    elif opcion == 8:
        salida = True
    else:
        print("Esa opcion no existe. Reingrese opcion: ")
        opcion = validar_opcion()
        ejecutar_opcion(opcion,salida)
    return salida
