import pymongo
from buildings_info import BuildingsInfo
from buildings_validator import BuildingsValidator
import requests

class TecnicoBuildings:
    def __init__(self, collection, initialize):
        self.campus_collection = collection
        self.validator = BuildingsValidator()

        if initialize:
            print("No collection named 'campus, creating it...")

            url = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/"
            response = requests.get(url)
            campus = response.json()

            info = BuildingsInfo()

            for c in campus:
                if info.getCampus(c['id']):
                    newUrl = url + c['id']
                    response = requests.get(newUrl)
                    campusInfo = response.json()

                    campusDict = {
                        'type': c['type'],
                        'id': int(c['id']),
                        'name': c['name'],
                        'containedSpaces': []
                    }

                    buildings = campusInfo['containedSpaces']

                    for b in buildings:
                        b_info = info.getBuilding(b['id'])

                        if b_info:
                            buildingDict = {
                                'type': b['type'],
                                'id': int(b['id']),
                                'name': b['name'],
                                'topLevelSpaceId': int(c['id']),
                                'botLat': float(b_info['botLat']),
                                'leftLng': float(b_info['leftLng']),
                                'topLat': float(b_info['topLat']),
                                'rightLng': float(b_info['rightLng'])
                            }

                            campusDict['containedSpaces'].append(buildingDict)

                    self.campus_collection.insert_one(campusDict)


    def addCampus(self, campusDict):
        documents = self.campus_collection.find({})

        if self.validator.checkCampus(campusDict, documents):
            self.campus_collection.insert_one(campusDict)
            return True
        return False

    def addBuilding(self, buildingDict):
        documents = self.campus_collection.find({})

        if self.validator.checkBuilding(buildingDict, documents):
            self.campus_collection.update_one({'id': buildingDict['topLevelSpaceId']},{'$push': {'containedSpaces': buildingDict}})
            return True
        return False

    def deleteSpace(self, spaceId):
        documents = self.campus_collection.find({})

        for campus in documents:
            if spaceId == campus['id']:
                self.campus_collection.delete_one({'id': spaceId})
                return True
            else:
                for containedSpace in campus['containedSpaces']:
                    if spaceId == containedSpace['id']:
                        self.campus_collection.update_one({'id': campus['id']},{'$pull': {'containedSpaces': {'id': spaceId}}})
                        return True
        return False
