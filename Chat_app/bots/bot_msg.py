from socketIO_client import SocketIO
import time

class BotMSG:
    def __init__(self, token):
        self.time=time.time()
        self.token = token
        socketIO = SocketIO('10.132.0.2', 5001)
        msg = input('Insira a mensagem a difundir pelo bot:\n> ')
        while True:
            time.sleep(5)
            socketIO.emit('bot_alert',{'building':self.token ,'value':msg})
            print(self.token)
