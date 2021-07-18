import service_drive, io, os
from googleapiclient.http import MediaIoBaseDownload
# mimeType='application/vnd.google-apps-document'
id_archivo = '1fwyn1BxJEIT9VYjqvHhFxx36DOzy0wNbs1nX4J6jm0Q'
nombre_archivo = 'fulano'
servicio = service_drive.obtener_servicio()
print(id_archivo)
print(nombre_archivo)
request = servicio.files().get_media(fileId=id_archivo)
fh = io.BytesIO()
downloader = MediaIoBaseDownload(fh, request)
done = False
while done is False:
    status, done = downloader.next_chunk()
    print("Download %d%%." % int(status.progress() * 100))