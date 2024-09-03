from asyncio.sslproto import AppProtocolState
from datetime import timedelta
from email.mime import image
from pyexpat import model
from flask import Flask, request, redirect, session, abort, url_for, make_response
from infrastructure.email_automation.gmail_service import GmailService
import os.path
import urllib.parse
import uuid
import logging
import requests
import json
import logging

gmail_service = GmailService()
def main():
    
    service = gmail_service.build_service()
    
    labels = gmail_service.list_labels(service)
    if not labels:
        print('No labels found.')
    else:
        print('Labels: ')
        for label in labels:
            print(f"Name: {label['name']}, ID: {label['id']}")

    keyword_labels = {
        'Label_6780004028642586479': ['bogota', 'BOGOTA D.C', 'Bogota'],
        'Label_450093062234346009': ['Cali', 'CALI', 'CALI VALLE DEL CAUCA'],
        'Label_195513504576196891': ['BUCARAMANGA', 'Bucaramanga', 'Snatander Bucaramanga']
    }
    
    messages = gmail_service.list_emails(service)
    if not messages:
        print('No new emails')
    else:
        for message in messages:
            msg_id = message['id']
            subject = gmail_service.get_email_subject(service, msg_id)
            sender = gmail_service.get_email_sender(service, msg_id)  # Obtener el remitente del correo
            
            for label_id, keywords in keyword_labels.items():
                for keyword in keywords:
                    if keyword.lower() in subject.lower():
                        print(f"Keyword '{keyword}' found in subject '{subject}'. Moving email to label ID '{label_id}'.")
                        gmail_service.move_email_to_label(service, msg_id, label_id)
                        
                        # Enviar respuesta automatica al remitente
                        auto_reply_subject = 'Confirmacion de Recepcion de Correo'
                        auto_reply_body = (
                            f'Hola,\n\n'
                            f'Hemos recibido tu correo con el asunto "{subject}". '
                            f'Nos pondremos en contacto contigo a la brevedad.\n\n'
                            f'Si lo deseas, puedes comunicarte con nosotros a traves de WhatsApp al siguiente numero: [Tu Numero de WhatsApp].\n\n'
                            f'Adjuntamos el catalogo de nuestros productos para tu referencia.\n\n'
                            f'Saludos cordiales,\n'
                            f'El equipo de ventas.'
                        )
                        if sender:  # Verificar si el remitente esta presente
                            gmail_service.send_email(service, sender, auto_reply_subject, auto_reply_body)
                        
                        break
if __name__ == '__main__':
    main()          
