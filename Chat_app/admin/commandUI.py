from inputs_validator import InputsValidator
import requests
from pprint import pprint

class CommandUI:
    def __init__(self, token):
        validor = InputsValidator()

        exited = False
        while not exited:
            print("Valid commands:")
            print("-'1' to define a build and their locations (latitude, longitude)")
            print("-'2' to list all users that are logged-in into the system")
            print("-'3' to list all users that are inside a certain building")
            print("-'4' to list the history of all the users movements and exchanged messages")
            print("-'exit' or 'q' to exit\n")

            cmd = input("> ")

            if cmd == '1':
                validor.checkBuilding(token)
            elif cmd == '2':
                response = requests.get("http://127.0.0.1:5000/api/admin/getall", json = {'token': token})
                result = response.json()
                key_list = list(result.keys())
                pprint(key_list)
                print("")

            elif cmd == '3':
                try:
                    _bid=input("Insert building id:\n> ")
                    bid= int(_bid)
                except ValueError:
                    print("NAN")
                    continue
                response = requests.get("http://127.0.0.1:5000/api/admin/inbuilding", json = {'token': token, 'id':bid})
                result = response.json()
                key_list = list(result.keys())
                pprint(key_list)
                print("")
            elif cmd == '4':

                response = requests.get("http://127.0.0.1:5000/api/admin/logs", json = {'token': token})
                pprint(response.json())
                print("")

            elif cmd.lower() == 'exit' or cmd.lower() == 'q':
                response = requests.get("http://127.0.0.1:5000/api/admin/logout", json = {'token': token})
                exited = True

            else:
                print("Invalid command!\n")
