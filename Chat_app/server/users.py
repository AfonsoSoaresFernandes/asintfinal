10.132.0.2import requests

class user1:
    numberOfUsers = 0

    def __init__(self, name, username, long ,lat,token,dist):
        self.name=name
        self.username=username
        self.long=long
        self.lat=lat
        self.token=token
        self.dist=dist

    def __str__(self):
        return "name : %s.\nusername : %s.\ntoken : %s.\n" % (self.name, self.username, self.token.access_token)


    def set(self,param, x):
        if param=="name":
            self.name=x
            return
        elif param=="number":
            self.number=x
            return
        elif param=="long":
            self.long=x
            return
        elif param=="lat":
            self.lat=x
            return
        elif param=="token":
            self.token=x
            return
        elif param=="dist":
            self.dist=x
            return
        else:
            print("Not a valid parameter")
            return

    def get(self,param):
        if param=="name":
            return self.name
        elif param=="number":
            return self.number
        elif param=="long":
            return self.long
        elif param=="lat":
            return self.lat
        elif param=="token":
            return self.token
        else:
            print("Not a valid parameter")
            return

    def user_to_dict(self):
        aux_dict={"name":self.name, "username":self.username, "long":self.long, "lat":self.lat, "token":self.token, "dist":self.dist}
        return aux_dict

def authok_rest(request,collection):
    if not 'token' in request.cookies:
        return "Nao ha sessao activa"
    else:
        aux = collection.find_one({"token":request.cookies['token']})
        if aux:
            return "ok"
        else:
            return "not"

def authok_sio(data):
    if not 'token' in data:
        return "not"
    else:
        response = requests.get('http://10.132.0.2:5000/user/exists',json={"token":data['token']})
        result = response.json()
        if result['id'] == "not":
            return "not"
        else:
            return "ok"
