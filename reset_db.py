import peewee
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
    {"when":"2020-04-05", "who":1, "room":4},
    {"when":"2020-04-07", "who":1, "room":4},
    {"when":"2020-04-05", "who":2, "room":7},
    {"when":"2020-04-05", "who":1, "room":3},
    {"when":"2020-04-06", "who":3, "room":4},
    {"when":"2020-04-05", "who":4, "room":7},
    {"when":"2020-04-05", "who":4, "room":2},
]

for bk in bookings:
    b = Booking(when=bk["when"], who=bk["who"], room=bk["room"])
    b.save()