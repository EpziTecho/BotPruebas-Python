from flask import Flask, request,jsonify,json
import sett
import services
import db.database as database 
from db.models import get_driver_idnumbers


app = Flask(__name__)

@app.route('/Bienvenido', methods=['GET'])
def bienvenido():
    return 'Bienvenido desde Flask!'

@app.route('/webhook', methods=['GET'])
def verificar_token():
    try:
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token == sett.token and challenge != None:
            return challenge
        else:
            return 'Token inválido',403
    
    except Exception as e:
        return e,403

@app.route('/webhook', methods=['POST'])
def recibir_mensajes():
    try:
        body = request.get_json()  # Obtener el cuerpo del mensaje
        print("Cuerpo completo del mensaje:", json.dumps(body, indent=4))  # Imprimir el mensaje completo
        body = request.get_json()
        entry = body['entry'][0]
        changes= entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        # number = services.replace_start(message['from'])
        number = message['from']
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.obtener_Mensaje_whatsapp(message)

        services.administrar_chatbot(text,number,messageId,name)
        return 'enviado',200
    
    except Exception as e:
        return 'no enviado' + str(e)

@app.route('/drivers/idnumbers', methods=['GET'])
def drivers_idnumbers():
    idnumbers = get_driver_idnumbers()
    return jsonify(idnumbers)

if __name__ == '__main__':
    database.test_db_connection()
    app.run(debug=True)