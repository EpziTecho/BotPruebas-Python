import requests
import sett
import json
def obtener_Mensajes_whatsapp(message):
    if 'type' not in message:
        text = 'mensaje no reconocido'
    
    typeMessage= message ['type']
    if typeMessage =='text':
        text = message['text']['body']
        return text
    
def enviar_Mensaje_whatsapp(data):
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {'Content-Type':'application/json','Authorization':'Bearer ' + whatsapp_token}
        response = requests.post(whatsapp_url, headers=headers, data=data)

        if response.status_code == 200:
            return 'Mensaje enviado'
        else:
            return 'Mensaje no enviado'
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

def buttonReply_Message(number,options,body,footer,sedd,messageId):
    buttons = []

    for i, option in enumerate(options):
        buttons.append(
            {
                "type  ": "reply",
                 "reply": {
                     "id": sedd +"_btn_"+str(i+1),
                     "text": option
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

def listReply_Message(number,options,body,footer,sedd,messageId):

    rows = []

    for i, option in enumerate(options):
        rows.append(
            {             
                "id": sedd +"_row_"+str(i+1),
                "reply": option,
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
            "button": "<Ver Opciones>",
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



def administrar_chatbot(text,number,messageId,name):
    text=text.lower() #mensaje que envia el usuario
    list = []

    data= text_Message(number,'Hola soy un chatbot, en que puedo ayudarte?')
    enviar_Mensaje_whatsapp(data)
