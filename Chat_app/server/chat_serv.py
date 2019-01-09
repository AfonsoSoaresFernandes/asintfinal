from flask import Flask, request, jsonify, send_from_directory, redirect,make_response
from flask_cors import CORS
import requests
import json
from users import user1, authok_rest, authok_sio
from flask_socketio import SocketIO, send, emit
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

clients = {}

@socketio.on('new_cli')
def new_client(_data):
    data = json.loads(_data)
    auth = authok_sio(data)
    clients[data['token']]=request.sid
    return "ok"

@socketio.on('disconnect')
def user_disconnect():

    for i,j in clients.items():
        if j==request.sid:
            del clients[i]
            response = requests.get('http://10.132.0.2:5000/user/disconnect',json={"token":i})
            break
    return "ok"
#WEB SocketIO
@socketio.on('sendmsg')
def handle_json(_data):
    data = json.loads(_data)
    auth = authok_sio(data)
    if auth == "ok":
        response = requests.get('http://10.132.0.2:5000/user/getall',json={"token":data['token'],"sender":data['username'],"msg":data['value']})
        result = response.json()
        key_list = list(result.keys())

        data['value'] = "From " + data['username']+ ": " + data['value']
        for x in key_list:
            x1 = clients[x]
            send(data['value'], room=x1)
    else:
        return "Invalid User"

@socketio.on('bot_alert')
def handle_bot(data):
    response = requests.get('http://10.132.0.2:5000/bot/alert',json={"building":data['building']})
    result = response.json()
    key_list = list(result.keys())
    data['value'] = "From Bot: " + data['value']
    for x in key_list:
        x1 = clients[x]
        send(data['value'], room=x1)
    return "ok"

if __name__ == '__main__':
    socketio.run(app, debug=True, host='10.132.0.2', port=5001, certfile='cert.pem', keyfile='key.pem')
