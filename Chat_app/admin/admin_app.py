from loginUI import LoginUI
from commandUI import CommandUI

if __name__ == "__main__":   
    token = LoginUI().loop()
    CommandUI(token)
   