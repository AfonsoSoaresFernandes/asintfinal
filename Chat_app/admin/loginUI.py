import getpass
import requests
import json

class LoginUI:
    def __init__(self):
        pass

    def loop(self):
        logged = False
        while not logged:
            name = input('Login name: ')
            password = getpass.getpass('Password: ')

            login_info = {
                'name': name,
                'password': password
            }

            url = "http://146.148.3.39:5000/api/admin"

            response = requests.get(url + "/login", json = login_info)

            response_json = response.json()

            try:
                token = response_json['token']
                logged = True
                print('Login successfull!\n')

            except:
                print('Error in login!\n')

        return token
