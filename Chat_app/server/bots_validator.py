class BotsValidator:
    def __init__(self):
        pass

    def checkBot(self, botDict, flag):
        keys = list(botDict.keys())

        if flag:
            args_list = ['acc_name', 'acc_pass', 'acc_building_id']
        else:
            args_list = ['acc_name', 'acc_pass']

        for value in args_list:
            if value in keys:
                pass
            else: 
                return False

        return True