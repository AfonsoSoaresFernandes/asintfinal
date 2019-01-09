class LogsValidator:
    def __init__(self):
        pass

    def checkLog(self, logDict):
        keys = list(logDict.keys())
        args_list = ['type', 'content', 'user_id','time']

        for value in args_list:
            if value in keys:
                pass
            else:
                return False

        if type(logDict['type']) is not str:
            return False

        if type(logDict['user_id']) is not str:
            return False

        if logDict['type'] == 'MOV':
            try:
                keys = list(logDict['content'].keys())
                size = len(keys)
                if size > 2:
                    return False
                args_list = ['lat', 'lng']

                for value in args_list:
                    if value in keys:
                        pass
                    else:
                        return False
            except KeyError:
                return False

        elif logDict['type'] == 'MSG':
            if type(logDict['content']) is not str:
                return False

        else:
            return False

        return True
