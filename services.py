import requests
import sett
import json
import time

from db.models import check_driver_id, get_driver_idnumbers


# Variable global para mantener un historial de estados
historial_de_estados = []

def obtener_Mensaje_whatsapp(message):
    if 'type' not in message :
        text = 'mensaje no reconocido'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'mensaje no procesado'
    
    
    return text

def enviar_Mensaje_whatsapp(data):
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + whatsapp_token}
        print("se envia ", data)
        response = requests.post(whatsapp_url, 
                                 headers=headers, 
                                 data=data)
        
        if response.status_code == 200:
            return 'mensaje enviado', 200
        else:
            return 'error al enviar mensaje', response.status_code
    except Exception as e:
        return e,403
    
def text_Message(number,text):
    data = json.dumps(
            {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": text
                }
            }
    )
    return data

def buttonReply_Message(number, options, body, footer, sedd, messageId, include_back=False, back_sedd=None):
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )
    
    if include_back:
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": back_sedd + "_back",
                    "title": "🔙 Volver"
                }
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data

def listReply_Message(number, options, body, footer, sedd,messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )
    return data

def document_Message(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
                "filename": filename
            }
        }
    )
    return data

def sticker_Message(number, sticker_id):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker_id
            }
        }
    )
    return data

def get_media_id(media_name , media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = sett.stickers.get(media_name, None)
    #elif media_type == "image":
    #    media_id = sett.images.get(media_name, None)
    #elif media_type == "video":
    #    media_id = sett.videos.get(media_name, None)
    #elif media_type == "audio":
    #    media_id = sett.audio.get(media_name, None)
    return media_id

def replyReaction_Message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    )
    return data
def replyText_Message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data

def handle_id_query(number, text):
    if text.isdigit():
        exists = check_driver_id(text)
        response_text = "Identificación encontrada." if exists else "Identificación no encontrada."
    else:
        response_text = "Por favor, envíe un número de identificación válido."
    return text_Message(number, response_text)

def administrar_chatbot(text, number, messageId, name):
    global historial_de_estados
    # Asegúrate de que el texto es una cadena, convertir a minúsculas y limpiar espacios
    text = str(text).strip().lower()
    actions = []  # Lista para guardar las acciones a enviar
    print("Mensaje del usuario:", text)  # Depuración para ver qué recibe exactamente el bot

    # Verificar estado actual
    current_state = historial_de_estados[-1]['text'] if historial_de_estados else "inicio"
    print("Estado actual:", current_state)  # Depuración para entender el estado

    if text == "hola":
        # Obtener todos los ID Numbers de la base de datos
        id_numbers = get_driver_idnumbers()  # Suponemos que esta función devuelve una lista de diccionarios
        id_list = ', '.join([str(id['idNumber']) for id in id_numbers])
        
        body = f"¡Hola! 👋 Bienvenido a nuestro servicio. Por favor, ingrese su número de identificación para continuar:\n\nIDs disponibles: {id_list}"
        
        historial_de_estados = [{"text": "esperando id", "number": number, "messageId": messageId, "name": name}]
        actions.append(text_Message(number, body))
    elif current_state == "esperando id":
        # Convertir texto a número antes de aplicar isdigit
        try:
            id_number = int(text)
            exists = check_driver_id(id_number) 
            print(check_driver_id(id_number))
            print ("existe", exists)
            if exists:
                body = "Bienvenido al sistema, aquí están los servicios disponibles."
                historial_de_estados.append({"text": "id confirmado", "number": number, "messageId": messageId, "name": name})
            else:
                body = "Usuario no encontrado. Por favor, intenta de nuevo."
            actions.append(text_Message(number, body))
            historial_de_estados = []  # Resetear estado tras respuesta
        except ValueError:
            body = "Número inválido. Por favor, intente nuevamente."
            actions.append(text_Message(number, body))
    else:
        body = "Lo siento, no entendí eso. ¿Puedes intentar de nuevo?"
        actions.append(text_Message(number, body))

    # Enviar todas las acciones acumuladas
    for action in actions:
        enviar_Mensaje_whatsapp(action)

#al parecer para mexico, whatsapp agrega 521 como prefijo en lugar de 52,
# este codigo soluciona ese inconveniente.
# def replace_start(s):
#     number = s[3:]
#     if s.startswith("521"):
#         return "52" + number
#     elif s.startswith("549"):
#         return "54" + number
#     else:
#         return s
        
