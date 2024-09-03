

# import os.path
# import pickle
# import base64 
# from turtle import width
# from google.auth import credentials
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from googleapiclient.discovery import build


# #Scope necesario para leer correos electronicos
# SCOPE = ['https://www.googleapis.com/auth/gmail.modify']

# def authenticate():
#     creds = None  
#     #Archivo donde se guardaran las credenciales despues de la autorizacion
#     token_path = 'token.pickle'
    
#     if os.path.exists(token_path)   and os.path.getsize(token_path) > 0 :
 
#         try:
#            with open(token_path, 'rb') as token:
#             creds = pickle.load(token)
#         except EOFError:
#             print("El archivo token.pickle esta vacio o corrupto. Necesita ser recreado.")
#         except Exception as e:
#             print(f"Ocurrio un error al cargar el archivo token.pickle: {e}")
            

#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPE)
#            creds = flow.run_local_server(port=0)
#            # Guarda las credenciales para la próxima vez
#         with open(token_path, 'wb') as token:
#              pickle.dump(creds, token)
               
#     return creds

# def list_labels(service):
#     results = service.users().labels().list(userId='me').execute()
#     labels = results.get('labels', [])
    
#     if not labels:
#         print('Not labels fund. ')
#     else:
#         print('Labels: ')
#         for label in labels:
#             print(f"Name: {label['name']}, ID: {label['id']}")

        
# def list_emails(service):
#     results = service.users().messages().list(userId='me', maxResults=10).execute()
#     messages = results.get('messages', [])
    
#     if not messages:
#         print('No new emails')
#     else:
#         print('Emails: ')
#         for message in messages:           
#             print(f"Message ID: {message['id']} ")
            
#     return messages

# def get_email_subject(service, msg_id):
#     message = service.users().messages().get(userId = 'me', id=msg_id, format='metadata', metadataHeaders=['Subject']).execute()
#     headers = message.get('payload', {}).get('headers', [])
#     subject = ''   
#     for header in headers:
#         if header['name'].lower() == 'subject':
#             subject = header['value']
#             break
#     return subject
    

# # def get_email_body(service, msg_id):
# #     message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
# #     payload = message.get('payload')
    
# #     if 'parts' in payload:
# #         for part in payload['parts']:
# #             if part['mimeType'] == 'text/plain':
# #                 data = part['body']['data']
# #                 body = base64.urlsafe_b64decode(data.encode('ASCII')).decode('utf-8')
# #                 break
# #     elif 'body' in payload:
# #         data = payload['body']['data']
# #         body = base64.urlsafe_b64decode(data.encode('ASCII')).decode('utf-8')
        
# #     return body

            
# def move_email_to_label(service, msg_id, label_id):
    
#    try:
#        service.users().messages().modify(userId='me', id=msg_id, body={'addLabelIds': [label_id]}).execute()
#        print(f'Correo {msg_id} movido a la etiqueta {label_id}')
#    except Exception as e:
#        print(f'Error al mover el correo {msg_id} a la etiqueta {label_id}.')
            

# if __name__ == '__main__':
#     creds = authenticate()
    
#     service = build('gmail', 'v1', credentials = creds)
#     list_labels(service)

#     #Definir palabras clave
#     keyword_labels = {
        
#         'Label_8897253909475220351'  :['etb', 'ETB'],
#         'Label_2171219515373875425'  :['telefonica', 'TELEFONICA'], 
#         'Label_263027264935884269'   :['stres', 'S3']
#         }
#     messages = list_emails(service)
    

#     for message in messages:
#         msg_id = message['id']
#         subject = get_email_subject(service, msg_id)
    
    
#         for label_id, keywords in keyword_labels.items():
#             for keyword in keywords:
#                 if keyword.lower() in subject.lower():
#                     print(f"keyword '{keyword}' found in subject '{subject}'. Moving email to label ID '{label_id}'.")
#                     move_email_to_label(service, msg_id, label_id)
#                     break 
    
    






