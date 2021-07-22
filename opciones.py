import listado, creacion, subida, descarga, sincronizar, carpetasgen

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
        creacion.crear()
    elif opcion == 3:
        subida.archivo_subido()
    elif opcion == 4:
        descarga.main_descarga()
    elif opcion == 5:
        sincronizar.main_sinc()
    elif opcion == 6:
        carpetasgen.main_carpetas()
    elif opcion == 7:
        salida = True
    elif opcion == 8:
        salida = True
    else:
        print("Esa opcion no existe. Reingrese opcion: ")
        opcion = validar_opcion()
        ejecutar_opcion(opcion,salida)
    return salida