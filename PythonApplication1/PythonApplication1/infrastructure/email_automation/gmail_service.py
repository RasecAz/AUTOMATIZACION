from asyncio import IocpProactor
import json
import os.path
import pickle
import base64
import imageio
import cv2
import numpy as np
from http import client
from google import oauth2
from genericpath import isfile
from distutils.util import execute
from email import message
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.errors import HttpError
from PIL import Image
from io import BytesIO
from oauthlib.oauth2.rfc6749.endpoints import authorization
from requests_oauthlib import OAuth2Session

# Rutas a los archivos
prototxt_path = 'C:/Users/usuario/Downloads/deploy.prototxt.txt'
caffemodel_path = 'C:/Users/usuario/Downloads/mobilenet_iter_73000.caffemodel'



class GmailService:
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
    TOKEN_PATH = 'token.pickle'
    CREDENTIALS_PATH = 'credentials.json'
    ZOHO_TOKEN_PATH = 'zoho_token.pickle'
    
    def authenticate(self):
        creds = None
        
        if os.path.exists(self.TOKEN_PATH) and os.path.getsize(self.TOKEN_PATH) > 0:
            try:
                with open(self.TOKEN_PATH, 'rb') as token:
                    creds = pickle.load(token)
            except EOFError:
                print("El archivo token.pickle esta vacio o corrupto. Necesita ser recreado.")
            except Exception as e:
                print(f"Ocurrio un error al cargar el archivo token.pickle: {e}")

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error a autenticar el token: {e}")
                    if os.path.exists(self.TOKEN_PATH):
                        os.remove(self.TOKEN_PATH)
                    creds = None
            if not creds:
                flow = InstalledAppFlow.from_client_secrets_file(self.CREDENTIALS_PATH, self.SCOPES)
                creds = flow.run_local_server(port=0)
                with open(self.TOKEN_PATH, 'wb') as token:
                    pickle.dump(creds, token)
        
        return creds

    def build_service(self):
        creds = self.authenticate()
        return build('gmail', 'v1', credentials=creds)

    def list_labels(self, service):
        results = service.users().labels().list(userId='me').execute()
        return results.get('labels', [])

    def list_emails(self, service, max_results=10):
        results = service.users().messages().list(userId='me', maxResults=max_results).execute()
        return results.get('messages', [])

    def get_email_subject(self, service, msg_id):
        message = service.users().messages().get(userId='me', id=msg_id, format='metadata', metadataHeaders=['Subject']).execute()
        headers = message.get('payload', {}).get('headers', [])
        for header in headers:
            if header['name'].lower() == 'subject':
                return header['value']
        return ''

    def move_email_to_label(self, service, msg_id, label_id):
        try:
            service.users().messages().modify(userId='me', id=msg_id, body={'addLabelIds': [label_id]}).execute()
            print(f'Correo {msg_id} movido a la etiqueta {label_id}')
        except Exception as e:
            print(f'Error al mover el correo {msg_id} a la etiqueta {label_id}: {e}')
            
    def get_email_sender(self, service, msg_id):
        """Obtiene la direccion del remitente del correo."""
        message = service.users().messages().get(userId='me', id=msg_id, format='metadata', metadataHeaders=['From']).execute()
        headers = message.get('payload', {}).get('headers', [])
        for header in headers:
            if header['name'].lower() == 'from':
                return header['value']
        return ''
            
    def has_image_attachment(self, service, msg_id):
        message = service.users().messages().get(userId = 'me', id = msg_id).execute()
        parts = message.get('payload', {}).get('parts', [])
        
        for part in parts:
            if part.get('filename') and 'image/' in part.get('mimeType', ''):
                return True
        return False
    
    def get_image_attachment(self, service, msg_id):
        message = service.users().messages().get(userId='me', id=msg_id).execute()
        parts = message.get('payload', {}).get('parts', [])

        for part in parts:
            if part.get('filename') and 'image/' in part.get('mimeType', ''):
                att_id = part['body']['attachmentId']
                attachment = service.users().messages().attachments().get(userId='me', messageId=msg_id, id=att_id).execute()
                data = base64.urlsafe_b64decode(attachment['data'])
                return np.array(Image.open(IocpProactor.BytesIO(data)))
        return None
    
    
    def send_email(self, service, to, subject, body):
        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')      
        try:
            service.users().messages().send(userId = 'me', body = {'raw': raw}).execute()
            print(f'emali sent to {to} with subject "{subject}".')
        except HttpError as error:
            print(f'An error ocurred while sending email: {error}')
            


                  
            
        