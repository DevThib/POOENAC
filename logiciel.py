from math import sqrt,inf
from statistics import mean
from datetime import date
from typing import Self

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
        selectedBase = None
        minDist = inf
        for base in self.bases:
            d = self.distance(base, (xm, ym, zm))
            if d < minDist:
                selectedBase = base
                minDist = d
        if selectedBase is None:  #vérifier qu'une base a bien été trouvée
            return False
        mission = Mission(zones)
        
        operator = selectedBase.get_operator()  # Transmission de la mission à l'opérateur
        if operator is None:
            return False
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

    def __init__(self:Self,payload,autonomy,base:Base):
        self.payload = payload
        self.autonomy = autonomy
        self.mission = None
        self.base = base

    def assigned_mission(self: Self, mission: Mission):
        self.mission = mission

    def start_mission(self:Self):
        if self.mission is None:
            return None
        return True
    

    def get_mission_status(self: Self, mission: Mission):
        zones_non_livrees = []
        zones_livrees:list = []
        for zone in mission.zones:
            heure = mission.status[zone]
            if heure is None:
                zones_non_livrees.append(zone)
            else:
                zones_livrees.append((zone, heure))
        if len(zones_non_livrees) == 0:
            return { "statut": "succès", "zones_livrees": zones_livrees, "zones_non_livrees": []}
        else:
            return {"statut": "échec", "zones_livrees": zones_livrees, "zones_non_livrees": zones_non_livrees}
                

    def get_autonomy(self:Self):
        return self.autonomy
    
    def get_payload(self: Self):
        return self.payload
    


class Operator:
    def __init__(self:Self,base : Base):
        self.base = base
        
    def start_new_mission(self: Self, mission: Mission):
        drone = self.select_drone(mission)
        if drone is None:
            return False
        drone.assign_mission(mission)
        drone.start_mission()
        return True
                    
    def select_drone(self: Self, mission: Mission):
        totalDistance = self.total_distance(mission)
        total_pills = sum( zone.nbPillsRequired for zone in mission.get_zones())
        for drone in self.base.get_drones():
            if drone.get_autonomy() >= totalDistance:
                if drone.get_payload() >= total_pills:
                    return drone
        return None
    
    def register(self:Self,logiciel:Logiciel):
        logiciel.register_operator(self)

    def total_distance(self:Self,mission:Mission):
        totalDistance = 0
        allPos = [self.base.get_cos()] + [z.get_cos() for z in mission.get_zones()] + [self.base.get_cos()]
        for i in range(len(allPos)-1):
                totalDistance += self.distance(allPos[i],allPos[i+1])
        return totalDistance
    
    def distance(self:Self,cosA:int,cosB:int):
        return sqrt((cosA[0]-cosB[0])**2+(cosA[1]-cosB[1])**2+(cosA[2]-cosB[2])**2)
    
