import getpass
import requests

class BotUI:
    def __init__(self):
        pass

    def loop(self):
        exited = False
        url = "http://10.132.0.2:5000/api/bot"

        while not exited:
            print("Valid commands:")
            print("-'1' to login")
            print("-'2' to create a bot accout")
            print("-'exit' or 'q' to exit\n")

            cmd = input("> ")

            if cmd == '1':
                acc_name = input("Bot login name: ")
                acc_pass = getpass.getpass('Bot password: ')

                acc_info = {
                    'acc_name': acc_name,
                    'acc_pass':  acc_pass
                }

                response = requests.get(url + '/login' , json = acc_info)
                response_json = response.json()

                try:
                    token = response_json['building']
                    print('Login successfull!\n')
                    return token

                except:
                    print('Error in login!\n')



            elif cmd == '2':
                acc_name = input("Bot login name: ")
                acc_pass = getpass.getpass('Bot password: ')
                input_holder = input("Bot Building ID: ")
                try:
                    acc_building_id = int(input_holder)
                except ValueError:
                    print('Building ID must be an integer')
                    continue

                acc_info = {
                    'acc_name': acc_name,
                    'acc_pass':  acc_pass,
                    'acc_building_id': acc_building_id
                }

                response = requests.post(url + '/account' , json = acc_info)
                response_json = response.json()
                print(response_json)

            elif cmd.lower() == 'exit' or cmd.lower() == 'q':
                exit()
            else:
                print("Invalid command!\n")
