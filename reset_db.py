
import peewee

import sys
import os
if os.path.exists("book.db"):
  os.remove("book.db")
else:
  print("The file does not exist") 
  sys.exit()

from app.models import User, Room, Booking


# Make users
users = [
    {"name":"David R.", "email":"david.roesel@epfl.ch", "password-plain":"horsefish"},
    {"name":"Maksim E.", "email":"maksim.eremchev@epfl.ch", "password-plain":"catmouse"},
    {"name":"Olesia A.", "email":"olesia.altunina@epfl.ch", "password-plain":"ponydog"},
    {"name":"Serhii K.", "email":"sergey.kulik@epfl.ch", "password-plain":"birdsnake"},
]

for user in users:
    u = User.create(name=user["name"], email=user["email"], password_hash="placeholder")
    u.set_password(user["password-plain"])
    u.save()

# Make rooms
rooms = [
["BM1118",1,"BM",],
["BM1117",1,"BM",],
["BM1116",1,"BM",],
["BM1115",1,"BM",],
["BM1114",1,"BM",],
["BM1113",1,"BM",],
["BM2118",2,"BM",],
["BM2117",2,"BM",],
["BM2116",2,"BM",],
["BM2115",2,"BM",],
["BM2114",2,"BM",],
["BM2113",2,"BM",],
["BM3118",3,"BM",],
["BM3117",3,"BM",],
["BM3116",3,"BM",],
["BM3115",3,"BM",],
["BM3114",3,"BM",],
["BM3113",3,"BM",],
["BM4118",4,"BM",],
["BM4117",4,"BM",],
["BM4116",4,"BM",],
["BM4115",4,"BM",],
["BM4114",4,"BM",],
["BM4113",4,"BM",],
["BM5118",5,"BM",],
["BM5117",5,"BM",],
["BM5116",5,"BM",],
["BM5115",5,"BM",],
["BM5114",5,"BM",],
["BM5113",5,"BM",],
["BP1118",1,"BP",],
["BP1117",1,"BP",],
["BP1116",1,"BP",],
["BP1115",1,"BP",],
["BP1114",1,"BP",],
["BP1113",1,"BP",],
["BP2118",2,"BP",],
["BP2117",2,"BP",],
["BP2116",2,"BP",],
["BP2115",2,"BP",],
["BP2114",2,"BP",],
["BP2113",2,"BP",],
["BP3118",3,"BP",],
["BP3117",3,"BP",],
["BP3116",3,"BP",],
["BP3115",3,"BP",],
["BP3114",3,"BP",],
["BP3113",3,"BP",],
["BP4118",4,"BP",],
["BP4117",4,"BP",],
["BP4116",4,"BP",],
["BP4115",4,"BP",],
["BP4114",4,"BP",],
["BP4113",4,"BP",],
["BP5118",5,"BP",],
["BP5117",5,"BP",],
["BP5116",5,"BP",],
["BP5115",5,"BP",],
["BP5114",5,"BP",],
["BP5113",5,"BP",],
["SV1118",1,"SV",],
["SV1117",1,"SV",],
["SV1116",1,"SV",],
["SV1115",1,"SV",],
["SV1114",1,"SV",],
["SV1113",1,"SV",],
["SV2118",2,"SV",],
["SV2117",2,"SV",],
["SV2116",2,"SV",],
["SV2115",2,"SV",],
["SV2114",2,"SV",],
["SV2113",2,"SV",],
["SV3118",3,"SV",],
["SV3117",3,"SV",],
["SV3116",3,"SV",],
["SV3115",3,"SV",],
["SV3114",3,"SV",],
["SV3113",3,"SV",],
["ME1118",1,"ME",],
["ME1117",1,"ME",],
["ME1116",1,"ME",],
["ME1115",1,"ME",],
["ME1114",1,"ME",],
["ME1113",1,"ME",],
["ME2118",2,"ME",],
["ME2117",2,"ME",],
["ME2116",2,"ME",],
["ME2115",2,"ME",],
["ME2114",2,"ME",],
["ME2113",2,"ME",],
["ME3118",3,"ME",],
["ME3117",3,"ME",],
["ME3116",3,"ME",],
["ME3115",3,"ME",],
["ME3114",3,"ME",],
["ME3113",3,"ME",],
["CH1118",1,"CH",],
["CH1117",1,"CH",],
["CH1116",1,"CH",],
["CH1115",1,"CH",],
["CH1114",1,"CH",],
["CH1113",1,"CH",],
["CH2118",2,"CH",],
["CH2117",2,"CH",],
["CH2116",2,"CH",],
["CH2115",2,"CH",],
["CH2114",2,"CH",],
["CH2113",2,"CH",],
["CH3118",3,"CH",],
["CH3117",3,"CH",],
["CH3116",3,"CH",],
["CH3115",3,"CH",],
["CH3114",3,"CH",],
["CH3113",3,"CH",],
["CH4118",4,"CH",],
["CH4117",4,"CH",],
["CH4116",4,"CH",],
["CH4115",4,"CH",],
["CH4114",4,"CH",],
["CH4113",4,"CH",],
["CH5118",5,"CH",],
["CH5117",5,"CH",],
["CH5116",5,"CH",],
["CH5115",5,"CH",],
["CH5114",5,"CH",],
["CH5113",5,"CH",]
]

for ri in rooms:
    r = Room(name=ri[0], floor=ri[1], building=ri[2])
    try:
        r.save()
        print("Success!")
    except peewee.IntegrityError:
        pass

# Make demo bookings

bookings = [
    {"when":"2020-04-05-AM", "who":1, "room":1, "status":"approved"},
    {"when":"2020-04-05-AM", "who":2, "room":2, "status":"approved"},
    {"when":"2020-04-05-AM", "who":3, "room":3, "status":"approved"},
    {"when":"2020-04-08-AM", "who":3, "room":0, "status":"approved"},
    {"when":"2020-04-05-PM", "who":1, "room":35, "status":"approved"},
    {"when":"2020-04-06-PM", "who":3, "room":36, "status":"denied"},
    {"when":"2020-04-05-PM", "who":4, "room":37, "status":"pending"},
    {"when":"2020-04-05-PM", "who":4, "room":40, "status":"pending"},
]

for bk in bookings:
    b = Booking(when=bk["when"], who=bk["who"], room=bk["room"], status=bk["status"])
    b.save()