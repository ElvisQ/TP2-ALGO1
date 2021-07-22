# TP2-AyP1
Trabajo Practico N°2 Algoritmos y Programacion, catedra: Costa 

Integrantes: Nazareno Napolitano, Camila Fiorotto, Elvis Quispe


Listado y descargas de archivos (Nazareno Napolitano):
Librerías usadas: os, io, googleapiclient (descarga de archivos); os, time, Pandas (listado de archivos).
Para listar los archivos locales primero obtuve mi ruta de trabajo con os.getcwd(), segundo utilicé la función os.path.listdir(ruta_trabajo) para obtener los archivos. Con la librería Pandas le di formato de data frame con los parámetros nombre, extensión y última fecha de modificación. La librería time (función time.ctime()) se usó para convertir los floats devueltos por la función os.path.getmtime() en fechas con formato legible.
Para los archivos guardados en Google Drive usé la función files.list() de la API (Drive) con los mismos parámetros que en local (nombre: 'name', tipo de archivo: 'mimeType', última modificación: 'modifiedTime'). También fue necesaria la librería Pandas para el formato de data frame.
El programa muestra todas las subcarpetas que se encuentren en el directorio actual, permitiendo listar los contenidos de las mismas.
Para la descarga de archivos el usuario simplemente debe ingresar el nombre que su archivo tenga en su unidad de Drive. El programa verifica que exista y si es así lo descarga (toma su id y la usa en las funciones de descarga). Si el archivo es de los tipos docs, presentaciones, drawings, script, spreadsheet, jam, form o site es necesario usar la función files.export() para convertirlos en formatos más amigables (pdf, jpg, texto plano, etc). Caso contrario simplemente se usa get.media(). Una vez descargados se almacenan en la carpeta de trabajo. La librería os fue necesaria para obtener la ruta actual (os.getcwd()) y para crear el directorio de destino de los archivos (os.path.join(ruta_actual,'nombre de archivo')). La librería io es necesaria para descargar los archivos (io.BytesIO(), para la comprensión de contenido binario).


Creación y subida de archivos (Camila Fiorotto): 
Librerías utilizadas: os, apiclient (Subir los archivos).
Tanto para la creación y la subida se utilizó la librería ‘os’ para verificar la existencia del archivo. En caso de la creación, para que no de error al crear uno nuevo, y en el caso de la subida, sea válida la misma.
Subida de archivos: esta función le preguntará al usuario qué tipo de extensión posee el archivo y procederá a pedirle que ingrese el nombre o dirección que está ubicado el mismo. Aquí es cuando entra la librería de apiclient y ayuda a que se suba el archivo al drive.
Creación de archivos: El programa le preguntará al usuario qué tipo de extensión desea crear y procederá a preguntarle con qué nombre lo querrá llamar. Luego se llamará a la función de “subir” procedente de la función de subida de archivos para que suba el mismo.


Generación de carpetas, sincronización, actualización de entregas (Elvis Quispe): 
Librereia utilizadas: os, io, zipfile, base64, csv, pathlib, datetime, time.
Sincronización: 
La función de sincronizar permite al usuario poder actualizar los archivos locales como también remoto. Para esto fue fundamental el uso de la librería os y pathlib, ya que facilitó al acceso de las rutas de cada carpeta y archivo. Se evalúa en el directorio de trabajo cada carpeta y se verifica si corresponde al sistema de carpetas anidados de un parcial. Al acceder a la carpeta de cada alumno se hace una lista con el contenido y se empieza a comparar cada archivo en local con los que están en Drive. Para esto se utilizaron sets para comparar listas de archivos. Si hay archivos que existen tanto en local como en remoto se debe entonces comparar fecha de modificaciones, en caso de que un archivo no esté en local o en remoto pues este deberá actualizarse en el lugar que corresponda.
Sistema de carpetas:
La función de sistema de carpetas permite al usuario generar las carpetas local y remota de un determinado parcial. Para esto se tuvo que buscar los mails recibidos y mostrar los primeros 5 asuntos de mails, luego el usuario elige el mensaje y en caso de que no se encuentre puede actualizarlo. Luego a partir de la opcion se crea la carpeta local del parcial y se busca dentro del mensaje seleccionado el archivo .zip para descargar y utilizar los datos que hay en ella. Una vez que se descarga los archivos correspondientes se empieza a anidar las carpetas las crea en local y con el mismo procedimiento las crea en el Drive.
