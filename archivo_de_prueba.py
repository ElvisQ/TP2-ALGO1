from pathlib import Path
import os



direcotorio= os.listdir('parcial1')
print(direcotorio)
parcial=os.path.abspath('parcial1')
dir=Path(parcial).iterdir()
print(dir)
lista=list(dir)
for i in lista:
    stri=str(i)
    print(stri)
    spli=stri.split("\\")
    print(spli)
    ultimo=spli[-1]
    print(ultimo)
'''for d in dir:
    nuevo=str(d)
    print(nuevo)
    print(type(nuevo))
    if os.path.isdir(nuevo):
        print('si es')
    else:
        print('no es')'''

'''
print(next(dir,None))
viejo=next(dir,None)
nuevo= str(next(dir,None))
print(viejo)
print(type(viejo))
print(nuevo)
print(type(nuevo))'''