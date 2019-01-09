from bots_validator import BotsValidator
import pymongo
from passlib.hash import pbkdf2_sha256

class TecnicoBots():
    def __init__(self, collection):
        self.bots_collection = collection
        self.validator = BotsValidator()

    def addBot(self, botDict):
        if self.validator.checkBot(botDict, True):
            results = self.bots_collection.count_documents({'$or': [{'acc_name': botDict['acc_name']},{'acc_building_id': botDict['acc_building_id']}]})

            if results == 0:
                botDict['acc_pass'] = pbkdf2_sha256.hash(botDict['acc_pass'])
                self.bots_collection.insert(botDict)
                return True
            return False
        else:
            return False

    def authenticateBot(self, botDict):
        if self.validator.checkBot(botDict, False):
            result = self.bots_collection.find_one({'acc_name': botDict['acc_name']})

            if pbkdf2_sha256.verify(botDict['acc_pass'], result['acc_pass']):
                return result['acc_building_id']

        else:
            return False
