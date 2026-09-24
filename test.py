from logiciel import *

za = Zone("A",50,10,10,10)
zb = Zone("B",20,40,13,0)
zc = Zone("C",70,18,29,4)

ba = Base("A",0,0,0)
bb = Base("B",44,44,44)

da = Drone("Fatima",90,10,ba)
db = Drone("Haytem",140,150,ba)

dc = Drone("Trevor",60,80,bb)
de = Drone("Benoit",80,110,bb)

op = Operator("Yannick",ba)
ope = Operator("Jean-Michel",bb)

log = Logiciel([za,zb,zc],[op,ope],[ba,bb])

log.start_new_mission([zc,zb])

