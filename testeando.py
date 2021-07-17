import io 
import time
import base64
from googleapiclient.http import MediaIoBaseUpload
from Google import Create_Service
import driveservice


def construct_service(api_service):
    CLIENT_SERVICE_FILE = 'client_secret_drive.json'
    try: 
        if api_service == 'drive':
            API_NAME = 'drive'
            API_VERSION = 'v3'
            SCOPES = ['https://www.googleapis.com/auth/drive']
            return Create_Service(CLIENT_SERVICE_FILE,API_NAME,API_VERSION,SCOPES)

        elif api_service == 'gmail':
            API_NAME = 'gmail'
            API_VERSION = 'v1'
            SCOPES = ['https://mail.google.com/']
            return Create_Service(CLIENT_SERVICE_FILE,API_NAME,API_VERSION,SCOPES)
  
    except Exception as e:
        print(e)
        return None

drive_services = construct_service('drive')

response = drive_services.list(
    q="name='June 2019' and mimeType='application/vnd.google-apps.folder'",
    spaces='drive'
).execute()