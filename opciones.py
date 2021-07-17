import listado, creacion, subida

def validar_opcion() -> int:
    '''
    Pide el ingreso de una opción y verifica que sea numérica.
    '''
    opcion = input()
    while not opcion.isnumeric():
        opcion = input("Entrada no valida. Debe ingresar un numero: ")
    return int(opcion)

def ejecutar_opcion(opcion: int, salida: bool) -> bool:
    '''
    Recibe una opción numérica y ejecuta una función según lo elegido.
    '''
    if opcion == 1:
        listado.main_listado()
    elif opcion == 2:
        creacion.main_creacion()
    elif opcion == 3:
        subida.main_subida()
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
