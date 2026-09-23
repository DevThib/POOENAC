from math import sqrt,inf
from statistics import mean

class Logiciel:
    def __init__(self,zones:list,operators : list,bases : list):
        self.zones = zones
        self.operators = operators
        self.bases = bases
        self.missions :list = []

    def start_new_mission(self,zones:list):
        xm,ym,zm = (mean([z.get_cos()[0] for z in zones]),mean([z.get_cos()[1] for z in zones]),mean([z.get_cos()[2] for z in zones]))
        selectedBase = None
        minDist = inf
        for b in self.bases:
            d = self.distance(b,(xm,ym,zm))
            if d < minDist:
                selectedBase = b
                minDist = d

        b.get_operator().start_new_mission(Mission(zones))


        

    def add_zone(self,zone:Zone):
        self.zones.append(zone)
        #recalculer priorité

    def distance(self,base,cos):
        bc = base.get_cos()
        return sqrt((cos[0]-bc[0])**2+(cos[1]-bc[1])**2+(cos[2]-bc[2])**2)
    

class Zone:

    def __init__(self,name:str,nbMedicRequired :int,x:float,y:float,z:float):
        self.name = name
        self.nbMedicRequired = nbMedicRequired
        self.priority :int = 0
        self.x = x
        self.y = y
        self.z = z

    def get_cos(self):
        return (self.x,self.y,self.z)
    
class Base:

    def __init__(self, name:str,x:float,y:float,z:float,operator :Operator):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.drones :list = []
        self.operator = operator
    
    def get_cos(self):
        return (self.x,self.y,self.z)

    def get_operator(self):
        return self.operator

    def get_drones(self):
        return self.drones
    
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

    def get_zones(self):
        return self.zones

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

    def get_autonomy(self):
        return self.autonomy

class Operator:
    def __init__(self,base : Base):
        self.base = base

    def start_new_mission(self,mission :Mission):
        #calc de la distance totale de parcours pour sélectionner le drone
        totalDistance = 0
        allPos = [self.base.get_cos()] + [z.get_cos() for z in mission.get_zones()] + [self.base.get_cos()]
        for i in range(len(allPos)):
            if i != len(allPos)-1:
                totalDistance += self.distance(allPos[i],allPos[i+1])
        
        droneForOperation = None
        #durant la mission si on a plus d'autonomie on revient a ka base et n relance l'opération de l'opérateur sans les zones effectuées
        
        droneForOperation.start_mission()


    def register(self):
        pass

    def distance(self,cosA,cosB):
        return sqrt((cosA[0]-cosB[0]**2)+(cosA[1]-cosB[1]**2)+(cosA[2]-cosB[2]**2))
    

    


