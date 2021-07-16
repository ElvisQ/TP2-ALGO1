import listado, carpetasgen

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
        pass
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
