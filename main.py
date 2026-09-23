import time as t

class Logiciel:
    def __init__(self,zones:list):
        self.zones = zones
        self.missions :list = []

    def start_new_mission(self,zones:list):
        pass

    def add_zones(self,zone:Zone):
        self.zones.append(zone)
        #recalculer priorité
    
    def create_missions(self):
        pass


class Zone:

    def __init__(self,name:str,nbMedicRequired :int):
        self.name = name
        self.nbMedicRequired = nbMedicRequired
        self.priority :int = 0
    
class Base:

    def __init__(self, name:str,x:float,y:float,z:float):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.drones :list = []
    
    
class Mission:
    def __init__(self,zones: list):
        self.zones = zones
        self.status :dict = {}

        for z in zones:
            self.status[z] = None
        
    def set_status(self,zone:Zone,hour):
        self.status[zone] = hour

    def get_status(self,zone):
        return self.status[zone] != None

class Drone:

    def __init__(self,payload,autonomy,base:Base):
        self.payload = payload
        self.autonomy = autonomy
        self.mission = None
        self.base = base

    def assign_mission(self):
        pass

    def start_mission(self):
        pass

    def get_mission_status(self):
        pass
    

    

    


