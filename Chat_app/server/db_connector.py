import pymongo
from tecnico_buildings import TecnicoBuildings
from tecnico_bots import TecnicoBots
from tecnico_logs import TecnicoLogs

class DB_Conector:
    def __init__(self, db_name):
        client = pymongo.MongoClient("mongodb+srv://asint:asint@asint-3tsob.gcp.mongodb.net/test?retryWrites=true")
        #client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
        db = client[db_name]
        dbs = client.list_database_names()

        if db_name in dbs:
            print("Database '%s' exists, loading it..." % (db_name))
        else:
            print("There is no database named '%s', creating it... " % (db_name))

        if 'campus' in db.collection_names():
            self.buildings_db = TecnicoBuildings(db['campus'], False)
        else:
            self.buildings_db = TecnicoBuildings(db['campus'], True)

        self.bots_db = TecnicoBots(db['bots'])
        self.logs_db = TecnicoLogs(db['logs'])

    def addCampus(self, campusDict):
        return self.buildings_db.addCampus(campusDict)

    def addBuilding(self, buildingDict):
        return self.buildings_db.addBuilding(buildingDict)

    def deleteSpace(self, spaceId):
        return self.buildings_db.deleteSpace(spaceId)

    def addBot(self, botDict):
        return self.bots_db.addBot(botDict)

    def authenticateBot(self, botDict):
        return self.bots_db.authenticateBot(botDict)

    def addLog(self, logDict):
        return self.logs_db.addLog(logDict)

    def getLogs(self):
       return self.logs_db.getLogs()
