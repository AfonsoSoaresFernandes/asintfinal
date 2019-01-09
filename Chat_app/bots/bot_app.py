from botUI import BotUI
from bot_msg import BotMSG

if __name__ == "__main__":
    token = BotUI().loop()
    BotMSG(token)
    