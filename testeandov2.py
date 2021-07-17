import time  
import io 
import base64
from googleapiclient.http import MediaIoBaseUpload
from Google import Create_Service


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


def search_email(service, query_string, label_ids = []):
    try:
        message_list_response = service.users().messages().list(
            userId = 'me',
            labelIds = label_ids,
            q = query_string
        ).execute()

        message_items = message_list_response.get('messages')
        nextPageToken = message_list_response.get('nextPageToken')

        while nextPageToken:
            message_list_response = service.users().messages().list(
                userId = 'me',
                labelIds = label_ids,
                q  =query_string,
                pageToken = nextPageToken
            ).execute()

            message_items.extend(message_list_response.get('messages'))
            nextPageToken = message_list_response.get('nextPageToken')
        return message_items

    except Exception as e:
        return None


def buscar_asunto():
    servicio= service_gmail.obtener_servicio()
    resultados = servicio.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    mensajes= resultados.get('messages',[])

    for mensaje in mensajes:
        msg=servicio.users().messages().get(userId='me', id= mensaje['id']).execute()


    headers = msg["payload"]["headers"]
    for i in headers:
        nameindict = i["name"]
        if nameindict == "Subject":
            print(i["value"])
        if nameindict == "Date":
            print(i["value"])

            return headers

def get_message_detail(service, message_id, format = 'metadata', metadata_headers=[]):
    try:
        message_detail = service.users().messages().get(
            userId = 'me',
            id = message_id,
            format = format,
            metadataHeaders = metadata_headers

        ).execute()
        return message_detail

    except Exception as e:
        print(e)
        return None



def create_folder_in_drive(service,folder_name,parent_folder=[]):
    file_metadata = {
        'name': folder_name,
        'parents': parent_folder,
        'mimeType': 'application/vnd.google-apps.folder'
    }

    file = service.files().create(body = file_metadata, fields = 'id').execute()
    return file




"""
Chequea si tiene archivos adjuntos
"""

def has_attachment():

    gmail_service = construct_service('gmail')
    drive_services = construct_service('drive')

    query_string = 'has:attachment'
    email_messages = search_email(gmail_service, query_string,['INBOX'])
    print(email_messages)

    return email_messages, gmail_service,drive_services






"""
Descarga el email y crea las carpetas en el drive
"""

def upload_email_drive():

    email_messages,gmail_service,drive_services = has_attachment()
   
    for email_message in email_messages:
        messageId = email_message['threadId']
        message_subject = '(No subject) ({0})'.format(messageId)
        messageDetail = get_message_detail(
            gmail_service, email_message['id'],
            format='full',
            metadata_headers = ['parts'])
        messageDetailPayload = messageDetail.get('payload')
        
        for item in messageDetailPayload['headers']:
            if item ['name'] == 'Subject':
                if item ['value']:
                    messageSubject = '{0} ({1})'.format(item['value'],messageId)
                else:
                    messageSubject = '(No subject ({0}))'.format(messageId)

    folder_id = create_folder_in_drive(drive_services, messageSubject)['id']

    if 'parts' in messageDetailPayload:
        for mesgPayload in messageDetailPayload['parts']:
            mime_type = mesgPayload['mimeType']
            file_name = mesgPayload['filename']
            body = mesgPayload['body']

            if 'attachmentId' in body:
                attachment_id = body['attachmentId']

                response = gmail_service.users().messages().attachments().get(    
                    userId = 'me',                                                
                    messageId = email_message['id'],                              
                    id = attachment_id                                            
                ).execute()                                                       

                file_data = base64.urlsafe_b64decode(                             #sacado de google
                    response.get('data'))                                         #sacado de google

                fd = io.BytesIO(file_data)                                        #sacado de google       

                file_metadata = {                                                 #sacadp de google
                    'name': file_name,                                           #sacado de google
                    'parents': [folder_id]                                       #sacado de google
                }

                media_body = MediaIoBaseUpload(fd, mimetype=mime_type, chunksize=1024*1024, resumable = True)

                file = drive_services.files().create(
                    body = file_metadata,
                    media_body = media_body,
                    fields = 'id'
                ).execute()

upload_email_drive()