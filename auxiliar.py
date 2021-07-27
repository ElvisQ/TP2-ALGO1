import service_drive, service_gmail, os

RUTA = os.getcwd()
SERV_GM = service_gmail.obtener_servicio()
SERV_DR = service_drive.obtener_servicio()
EXPORT = {'application/vnd.google-apps.presentation':'application/vnd.oasis.opendocument.presentation',
                    'application/vnd.google-apps.document':'application/pdf',
                    'application/vnd.google-apps.drawing':'image/jpeg',
                    'application/vnd.google-apps.script':'application/vnd.google-apps.script+json',
                    'application/vnd.google-apps.spreadsheet':'application/pdf',
                    'application/vnd.google-apps.drawing':'image/jpeg',
                    'application/vnd.google-apps.jam':'application/pdf',
                    'application/vnd.google-apps.form':'application/pdf',
                    'application/vnd.google-apps.site':'text/plain'
}