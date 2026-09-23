from math import sqrt,inf
from statistics import mean
from datetime import date
from typing import Self,Optional
    

class Zone:

    def __init__(self:Self,name:str,nbPillsRequired :int,x:float,y:float,z:float):
        self.name = name
        self.nbPillsRequired = nbPillsRequired
        self.priority = 0
        self.x = x
        self.y = y
        self.z = z

    def get_cos(self:Self):
        return (self.x,self.y,self.z)
    
class Base:

    def __init__(self:Self, name:str,x:float,y:float,z:float):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.drones:list = []
        self.operator = None
    
    def get_cos(self:Self):
        return (self.x,self.y,self.z)

    def get_operator(self:Self):
        return self.operator

    def get_drones(self:Self):
        return self.drones
    
    def add_drone(self, drone):   #pour avoir des drones dans la base
        self.drones.append(drone)

    def get_name(self):
        return self.name

    def set_operator(self,operator):
        self.operator = operator
    
class Mission:
    def __init__(self:Self,zones: list):
        self.zones = zones
        self.status = {zone: None for zone in zones}
        
    def set_status(self:Self,zone:Zone,hour):
        self.status[zone] = hour

    def get_status(self:Self,zone:Zone):
        return self.status[zone] != None

    def get_zones(self:Self):
        return self.zones


class Drone:

    def __init__(self:Self,name:str,payload,autonomy,base:Base):
        self.payload = payload
        self.autonomy = autonomy
        self.mission:Optional[Mission] = None
        self.base = base
        self.name = name

        self.base.add_drone(self) #on assigne le drone a la base car il ne peut y en avoir qu'un

    def assign_mission(self: Self, mission: Mission):
        self.mission = mission

    def start_mission(self:Self):
        print("Mission started")

    def get_mission_status(self: Self, mission: Mission):
        NonDeliveredZones:list = []
        deliveredZones:list = []
        for zone in mission.zones:
            heure = mission.status[zone]
            if heure is None:
                NonDeliveredZones.append(zone)
            else:
                deliveredZones.append((zone, heure))
        if len(NonDeliveredZones) == 0:
            return { "statut": "succès", "zones_livrees": deliveredZones, "zones_non_livrees": []}
        else:
            return {"statut": "échec", "zones_livrees": deliveredZones, "zones_non_livrees": NonDeliveredZones}
                

    def get_autonomy(self:Self):
        return self.autonomy
    
    def get_payload(self: Self):
        return self.payload
    
    def get_name(self):
        return self.name


class Operator:
    def __init__(self:Self,name:str,base : Base):
        self.base = base
        self.name = name

        self.base.set_operator(self)#on assigne directement l'opérateur a la base car il n'y en a qu'un
        
    def start_new_mission(self: Self, mission: Mission):
        drone:Drone = self.select_drone(mission)

        if drone == None:
            print("Aucun drone n'a les capacités...")
        else:
            print("Drone sélectionné : "+drone.get_name())

        if drone is None:
            return False
        drone.assign_mission(mission)
        drone.start_mission()
        return True
                    
    def select_drone(self: Self, mission: Mission):
        totalDistance = self.total_distance(mission)
        totalPills = sum(zone.nbPillsRequired for zone in mission.get_zones())

        print("Distance à parcourir : "+str(totalDistance)+"\nCharge marchande : "+str(totalPills))
    
        for drone in self.base.get_drones():
            if drone.get_autonomy() >= totalDistance and drone.get_payload() >= totalPills:
                return drone
        return None
    
    def total_distance(self:Self,mission:Mission):
        totalDistance = 0
        allPos = [self.base.get_cos()] + [z.get_cos() for z in mission.get_zones()] + [self.base.get_cos()]
        for i in range(len(allPos)-1):
                totalDistance += self.distance(allPos[i],allPos[i+1])
        return totalDistance
    
    def distance(self:Self,cosA:list,cosB:list):
        return sqrt((cosA[0]-cosB[0])**2+(cosA[1]-cosB[1])**2+(cosA[2]-cosB[2])**2)

    def get_name(self):
        return self.name

class Logiciel:
    def __init__(self:Self,zones:list,operators : list,bases : list):
        self.zones = zones
        self.operators = operators
        self.bases = bases
        self.missions :list = []


    def start_new_mission(self: Self, zones: list):
        xm = mean([z.get_cos()[0] for z in zones])
        ym = mean([z.get_cos()[1] for z in zones])
        zm = mean([z.get_cos()[2] for z in zones])

        selectedBase:Optional[Base] = None
        minDist:float = inf
        for base in self.bases:
            d = self.distance(base, (xm, ym, zm))
            if d < minDist:
                selectedBase = base
                minDist = d
        if selectedBase is None:  #vérifier qu'une base a bien été trouvée
            return False
        print("Base séléctionnée : "+selectedBase.get_name())
        mission = Mission(zones)
        
        operator:Operator = selectedBase.get_operator()  # Transmission de la mission à l'opérateur
        if operator is None:
            return False
        print(operator.get_name()+" s'occupe de la mission")
        success = operator.start_new_mission(mission)
        if success:
            self.missions.append(mission)
        return success

    def add_zone(self:Self,zone:Zone):
        self.zones.append(zone)
        #recalculer priorité

    def distance(self:Self,base,cos):
        bc = base.get_cos()
        return sqrt((cos[0]-bc[0])**2+(cos[1]-bc[1])**2+(cos[2]-bc[2])**2)
    
    
    def register_operator(self: Self, operator:Operator):
        if operator not in self.operators:
            self.operators.append(operator)