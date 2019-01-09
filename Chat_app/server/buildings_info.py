class BuildingsInfo:
    def __init__(self):
        self.info = {}
        # Campus Tecnológico e Nuclear
        self.info['2448131392438'] = None

        # Campus Tagus
        self.info['2448131360898'] = None

         # Campus Alameada
        self.info['2448131360897'] = {}

        # Buildings in Alameda

        # Central
        self.info['2448131360897']['2448131361060'] = {
            'botLat': 38.736287, 
            'leftLng': -9.139606,
            'topLat': 38.737175,
            'rightLng': -9.139061
        }
        # Torre Norte
        self.info['2448131360897']['2448131361091'] = {
            'botLat': 38.737522, 
            'leftLng': -9.138948,
            'topLat': 38.737875,
            'rightLng': -9.138213
        }

        # Torre Sul
        self.info['2448131360897']['2448131361074'] = {
            'botLat': 38.735733,
            'leftLng': -9.138769,
            'topLat': 38.736279,
            'rightLng': -9.138002
        }

        # Civil
        self.info['2448131360897']['2448131361042'] = {
            'botLat': 38.736924,
            'leftLng': -9.140412,
            'topLat': 38.737893,
            'rightLng': -9.140018
        }

        # Pavilhão de matemática
        self.info['2448131360897']['2448131361119'] = {
            'botLat': 38.735493,   
            'leftLng': -9.140006,
            'topLat': 38.735654,
            'rightLng': -9.139610
        }

        # Complexo interdisciplinar
        self.info['2448131360897']['2448131361035'] = {
            'botLat': 38.735687,
            'leftLng': -9.140237,
            'topLat': 38.736378,
            'rightLng': -9.140123
        }

        # Pavilhão de mecanica III
        self.info['2448131360897']['2448131361155'] = {
            'botLat': 38.737159,
            'leftLng': -9.137167,
            'topLat': 38.737560,
            'rightLng': -9.136818
        }

        # Pavilhão informatica III
        self.info['2448131360897']['2448131361129'] = {
            'botLat': 38.737279,
            'leftLng': -9.137681,
            'topLat': 38.737774, 
            'rightLng': -9.137291
        }
        
        # Associação de Estudantes
        self.info['2448131360897']['2448131384238'] = {
            'botLat': 38.736060,
            'leftLng': -9.137303,
            'topLat': 38.736568,
            'rightLng': -9.136839
        }
    
    def getCampus(self, campusID):
        try:
            return self.info[campusID]
        except:
            return None

    def getBuilding(self, buildingID):
        IDs = list(self.info)

        for campusID in IDs:
            try:
                return self.info[campusID][buildingID]
            except:
                pass

        return None
        
    