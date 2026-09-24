from math import sqrt,inf
from statistics import mean
from datetime import date
from typing import Self,Optional
import pint 
import icontract

ureg = pint.UnitRegistry()

class Zone:
    
    @icontract.require(lambda nbPillsRequired: nbPillsRequired >= 0)
    def __init__(self:Self,name:str,nbPillsRequired :int,x:float,y:float,z:float):
        self.name = name
        self.nbPillsRequired = nbPillsRequired
        self.priority:int = 0
        self.x = x
        self.y = y
        self.z = z

    def get_cos(self:Self):#récupération des coordonnées
        return (self.x,self.y,self.z)

    def set_priority(self,priority:int):
        self.priority = priority
    
    def get_nbPillsRequired(self):
        return self.nbPillsRequired

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
        self.status = {zone: None for zone in zones}#Si la zone n'a pas encore été livrée,on met None,sinon on met l'heure de livraison
        
    def set_status(self:Self,zone:Zone,hour):
        self.status[zone] = hour

    def get_status(self:Self,zone:Zone):
        return self.status[zone] != None#booléen : vrai si la zone a été livrée,faux sinon

    def get_zones(self:Self):
        return self.zones


class Drone:

    #@ureg.check(None,None,'[mass]','[length]',None)
    def __init__(self:Self,name:str,payload:pint.Quantity,autonomy:pint.Quantity,base:Base):
        self.payload = payload*ureg.kg
        self.autonomy = autonomy*ureg.km
        self.mission:Optional[Mission] = None
        self.base = base
        self.name = name

        self.base.add_drone(self) #on assigne le drone a la base car il ne peut y en avoir qu'un

    def assign_mission(self: Self, mission: Mission):
        self.mission = mission

    def start_mission(self:Self):
        print(self.name + " est parti en mission")

    def get_mission_status(self: Self, mission: Mission):
        NonDeliveredZones:list = []
        deliveredZones:list = []
        for zone in mission.zones:#une zone qui a une heure de livraison a été livrée
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
       
        zonesToAttribute:list = mission.get_zones().copy()
        startingPoint:tuple = self.base.get_cos()
        totalPills = sum(zone.nbPillsRequired for zone in mission.get_zones())*ureg.kg

        print("Distance à parcourir : "+str(self.total_distance(mission))+"\nCharge marchande : "+str(totalPills))

        idrone = 0
        izone = 0
        while totalPills > 0:#on parcourt les drones et on change dès qu'une drone a atteint sa capcité ou distance max
            if idrone == len(self.base.get_drones()):
                print("Pas assez de drones disponibles,manque de budget...,échec de la mission")
                break
            dr = self.base.get_drones()[idrone]
            droneDist = 0
            droneLoad = 0
            dist = self.distance(startingPoint,zonesToAttribute[izone].get_cos())
            load = zonesToAttribute[izone].get_nbPillsRequired()*ureg.kg
            z = []
            print("Lancement d'un nouveau drone")
            while droneDist+dist < dr.get_autonomy() and droneLoad+load < dr.get_payload():
                z.append(zonesToAttribute[izone])
                droneDist += dist
                droneLoad += load
                totalPills -= load
                startingPoint = zonesToAttribute[izone].get_cos()
                izone += 1
                if totalPills <= 0:break
                dist = self.distance(startingPoint,zonesToAttribute[izone].get_cos())
                load = zonesToAttribute[izone].get_nbPillsRequired()*ureg.kg
            if z != []:
                dr.assign_mission(Mission(z))
                dr.start_mission()
            else:
                print("Ce drone n'est pas adapté :(")
            idrone += 1
            z = []
       
    def total_distance(self:Self,mission:Mission):
        totalDistance = 0*ureg.km
        allPos = [self.base.get_cos()] + [z.get_cos() for z in mission.get_zones()] + [self.base.get_cos()]
        for i in range(len(allPos)-1):
                totalDistance += self.distance(allPos[i],allPos[i+1])
        return totalDistance
    
    def distance(self:Self,coosA:tuple,coosB:tuple):#distance euclidienne
        return sqrt((coosA[0]-coosB[0])**2+(coosA[1]-coosB[1])**2+(coosA[2]-coosB[2])**2)*ureg.km

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
        minDist = inf*ureg.km
        for base in self.bases:#on prend la base en moyenne la plus proche des trois zones
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

    def distance(self:Self,base,cos):
        bc = base.get_cos()
        return sqrt((cos[0]-bc[0])**2+(cos[1]-bc[1])**2+(cos[2]-bc[2])**2)*ureg.km
    
    
    def register_operator(self: Self, operator:Operator):
        if operator not in self.operators:
            self.operators.append(operator)
