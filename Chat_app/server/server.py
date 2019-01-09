from functools import wraps
from flask import Flask, request, jsonify, send_from_directory, redirect,make_response
from flask_cors import CORS
from db_connector import DB_Conector
import fenixedu
from random import randint
import pymongo
from calculator import findDistance, in_building
from users import user1, authok_rest
import datetime
import time


app = Flask(__name__)
CORS(app)

#Initialize db connection
db = DB_Conector('asint')
token_dic = {}

client_db = pymongo.MongoClient("mongodb+srv://asint:asint@asint-3tsob.gcp.mongodb.net/test?retryWrites=true")
db2 = client_db['asint']
collection = db2['users']
buildings = db2['campus']
#autenticação
config = fenixedu.FenixEduConfiguration('1414440104755260', 'http://146.148.3.39:5000/user/logged', '/q2j/1VRazbkEeK3JnqgOanxPHfC6PKybkaTIoLmeZqQeGeNrfE/KgmnbnTTBYd1nnRsS5WqOhluCuXqxkH4NQ==', 'https://fenix.tecnico.ulisboa.pt/')
client_edu = fenixedu.FenixEduClient(config)
url = client_edu.get_authentication_url()


collection.delete_many({})
# IR BUSCAR AO HEADER AUTHORIZATION EM VEZ DE ENVIAR JSON

def admin_login_required(route_to_wrap):
    @wraps(route_to_wrap)
    def wrap(*args, **kwargs):
        info = request.get_json()

        if info:
            try:
                if info['token'] in list(token_dic.values()) and info['token'] == token_dic['admin']:
                    return route_to_wrap(*args, **kwargs)
                else:
                    return jsonify({'error': 'Permission denied!'}), 403

            except KeyError:
                return jsonify({'error': 'Permission denied!'}), 403
        else:
            return jsonify({'error': 'Permission denied!'}), 403

    return wrap

# ADMIN API
@app.route('/api/admin/login', methods = ['GET'])
def admin_login():
    login_info = request.get_json()
    if login_info:
        try:
            name = login_info['name']
            password = login_info['password']

            if name == 'admin' and password == '123':
                if 'admin' not in list(token_dic.keys()):
                    token_dic[name] = 'token_admin_' + str(randint(10000000,100000000))
                    return jsonify({'token': token_dic[name]}), 200
                else:
                    return jsonify({'error': 'User already logged!'}), 400
            else:
                return jsonify({'error': 'Wrong login information!'}), 400
        except KeyError:
             return jsonify({'error': 'Wrong format!'}), 400
    return jsonify({'error': 'No login information!'}), 400

@app.route('/api/admin/logout', methods = ['GET'])
@admin_login_required
def admin_logout():
    logout_info = request.get_json()

    if logout_info:
        try:
            token = logout_info['token']
            if token in list(token_dic.values()):
                token_dic.pop('admin')
                return jsonify({'status': 'Successfull logout!'}), 200
        except KeyError:
             return jsonify({'error': 'Wrong format!'}), 400
    return jsonify({'error': 'No parameters!'}), 400

@app.route('/api/admin/building', methods = ['POST'])
@admin_login_required
def admin_add_building():
    building_info = request.get_json()
    building_info.pop('token')

    if building_info:
        try:
            if building_info['type'] == 'CAMPUS':
                result = db.addCampus(building_info)

            elif building_info['type'] == 'BUILDING':
                result = db.addBuilding(building_info)

            if result:
                return jsonify({'status': 'Successfull'}), 200
            else:
                return jsonify({'status': 'Could not perform this action, some inputs are invalid!'}), 400
        except KeyError:
            return jsonify({'status': 'Missing parameters!'}), 400
    else:
        return jsonify({'error': 'No building information!'}), 400

@app.route('/api/admin/building', methods = ['DELETE'])
@admin_login_required
def admin_delete_building():
    building_info = request.get_json()
    building_info.pop('token')

    try:
        if building_info:
            result = db.deleteSpace(building_info['spaceId'])
            if result:
                return jsonify({'status': 'Successfull'}), 200
            else:
                return jsonify({'status': 'Could not perform this action, space ID does not exists!'}), 400
        else:
            return jsonify({'error': 'No building information!'}), 400
    except KeyError:
        return jsonify({'status': 'Missing parameters!'}), 400

@app.route('/api/admin/logs', methods = ['GET'])
@admin_login_required
def admin_get_logs():
    result = db.getLogs()
    return jsonify(result)

@app.route('/api/admin/getall', methods=['GET'])
@admin_login_required
def getall_admin():
    users = {}
    aux2 = collection.find({})
    for user in aux2:
        users[user['username']]=1
    return jsonify(users)

@app.route('/api/admin/inbuilding', methods=['GET'])
@admin_login_required
def inBuilding_admin():
    req = request.get_json()
    documents = buildings.find({})
    aux={}
    obj={}

    for campus in documents:
        if req['id'] == campus['id']:
            return
        else:
            for containedSpace in campus['containedSpaces']:
                if req['id'] == containedSpace['id']:
                    aux['leftLng']= containedSpace['leftLng']
                    aux['rightLng']= containedSpace['rightLng']
                    aux['topLat']= containedSpace['topLat']
                    aux['botLat']= containedSpace['botLat']
                    break
    if aux:
        aux2 = collection.find({})
        for user in aux2:
            if in_building(aux['leftLng'], aux['rightLng'],aux['topLat'], aux['botLat'],user['lat'], user['long']):
                obj[user['username']]=1
        return jsonify(obj)
    else:
        fail = {'id':'Invalid building'}
        return jsonify(fail)

#BOT API
@app.route('/api/bot/login', methods = ['GET'])
def bot_login():
    acc_info = request.get_json()

    if acc_info:
        result = db.authenticateBot(acc_info)
        if result:
            return jsonify({'building': result}), 400
        else:
            return jsonify({'error': 'Login failled!'}), 400
    else:
        return jsonify({'error': 'No bot account information!'}), 400

@app.route('/api/bot/account', methods = ['POST'])
def bot_account_creation():
    acc_info = request.get_json()

    if acc_info:
        result = db.addBot(acc_info)
        if result:
            return jsonify({'status': 'Bot created'}),200
        else:
            return jsonify({'status': 'Something already in use'}),400
    else:
        return jsonify({'error': 'No bot account information!'}), 400

#USER USER USER USER USER

#First page, redirects user/login2
@app.route('/', methods = ['GET'])
def user_login():
    return send_from_directory(directory='webpages',filename='index.html')

#this route redirects the user to fenix
@app.route('/user/login2', methods = ['GET'])
def user_login2():
    return redirect(url)

#First route after fenix autentication,logs user in the server and sets cookie for future comunications
@app.route('/user/logged', methods = ['GET'])
def user_logged():
    user2 = client_edu.get_user_by_code(request.args['code'])
    person = client_edu.get_person(user2)

    new_user=user1(person['name'], person['username'], 0,0,request.args['code'],10)
    new_user.numberOfUsers=new_user.numberOfUsers +1


    #INSERIR NA BASE DE DADOS
    collection.insert_one(new_user.user_to_dict())

    response = make_response(send_from_directory(directory='webpages',filename='authok.html'))
    response.set_cookie('token',request.args['code'])
    response.set_cookie('username',person['username'])
    return response

#main page with the user app
@app.route('/user/logged2', methods = ['GET'])
def user_logged2():
    auth = authok_rest(request,collection)

    if auth=="ok":
        return send_from_directory(directory='webpages',filename='main.html')
    else:
        return auth

@app.route('/user/exists' ,methods = ['GET'])
def user_exists():
    req = request.get_json()
    aux = collection.find_one({"token":req['token']})
    if aux:
        #PODEMOS ENVIAR SO UMA STRING COM OK EM VEZ DO DICIONARIO
        obj = {'name': aux['name'],'token': aux['token']}
        return jsonify(obj)
    else:
        return "not"

@app.route('/user/location',methods = ['POST'])
def set_location():
    req = request.get_json()
    if authok_rest(request ,collection)=="ok":
        ts = datetime.datetime.fromtimestamp(time.time()).isoformat()
        log = {"type":"MOV", "content":{"lat": req['lat'],"lng":req['long']}, "user_id":req['sender'], "time":ts}
        db.addLog(log)

        collection.update_one({"token":request.cookies['token']},{'$set':{"long":req['long'],"lat":req['lat']}})
        aux = collection.find_one({"token":request.cookies['token']})
        aux2 = collection.find({})
        obj ={}
        for user in aux2:
            if findDistance(aux['lat'],aux['long'] ,user['lat'], user['long']) <= aux['dist']:
                    obj[user['username']]=1
        return jsonify(obj)
    else:
        fail = {"id":"INVALID USER"}
        return jsonify(fail)

@app.route('/user/distance',methods = ['POST'])
def set_distance():
    req = request.get_json()
    if authok_rest(request ,collection)=="ok":
        if int(req['value'])<0:
            return "Não são permitidos numeros negativos"
        else:
            collection.update_one({"token":request.cookies['token']},{'$set':{"dist":int(req['value'])}})
            return "Distancia alterada com sucesso"
    else:
        return "Invalid User"

@app.route('/user/logout',methods = ['GET'])
def user_logout():
    if authok_rest(request ,collection)=="ok":
        collection.delete_one({"token":request.cookies['token']})
        return "ok"
    else:
        return "Invalid User"

@app.route('/user/disconnect',methods = ['GET'])
def user_disconnect():
    req = request.get_json()
    collection.delete_one({"token":req['token']})
    return "ok"

@app.route('/user/getall', methods = ['GET'])
def get_all():
    req = request.get_json()
    aux = collection.find_one({"token":req['token']})
    aux2 = collection.find({})
    obj ={}
    #log
    ts = datetime.datetime.fromtimestamp(time.time()).isoformat()
    log = {"type":"MSG", "content":req['msg'], "user_id":req['sender'],"time":ts}
    db.addLog(log)

    for user in aux2:
        if findDistance(aux['lat'],aux['long'] ,user['lat'], user['long']) <= aux['dist']:
            obj[user['token']]=1
    return jsonify(obj)


@app.route('/bot/alert', methods=['GET'])
def checkBuilding():
    req = request.get_json()

    documents = buildings.find({})
    aux={}
    obj={}
    for campus in documents:
        if req['building'] == campus['id']:
            return
        else:
            for containedSpace in campus['containedSpaces']:
                if req['building'] == containedSpace['id']:
                    aux['leftLng']= containedSpace['leftLng']
                    aux['rightLng']= containedSpace['rightLng']
                    aux['topLat']= containedSpace['topLat']
                    aux['botLat']= containedSpace['botLat']
                    break
    if aux:
        aux2 = collection.find({})
        for user in aux2:
            if in_building(aux['leftLng'], aux['rightLng'],aux['topLat'], aux['botLat'],user['lat'], user['long']):
                obj[user['token']]=1
        return jsonify(obj)
    else:
        fail = {'id':'Invalid building'}
        return jsonify(fail)

if __name__ == '__main__':
    app.run(host='10.132.0.2', port=5000)
