

def opciones()->int:
    print('1)Generar carpetas localmente')
    print('2)Generar carpetas en Google Drive')
    opcion=input('\nIngrese una opcion: ')
    while not opcion.isnumeric():
        opcion=input('\nError, Vuelva a ingresar: ')
    return int(opcion)



def main_carpetas()->None:
    opcion=opciones()
    if opcion==1:
        pass
    elif opcion==2:
        pass
