import peewee
from models import Room, Booking

#r = Room(name="BM4118", floor=1, building="BM").save()


#r = Room.select().where(Room.name=='BM4118').get()
#print(r.building)

# rs = [
# ["BM1118",1,"BM",],
# ["BM1117",1,"BM",],
# ["BM1116",1,"BM",],
# ["BM1115",1,"BM",],
# ["BM1114",1,"BM",],
# ["BM1113",1,"BM",],
# ["BM2118",2,"BM",],
# ["BM2117",2,"BM",],
# ["BM2116",2,"BM",],
# ["BM2115",2,"BM",],
# ["BM2114",2,"BM",],
# ["BM2113",2,"BM",],
# ["BM3118",3,"BM",],
# ["BM3117",3,"BM",],
# ["BM3116",3,"BM",],
# ["BM3115",3,"BM",],
# ["BM3114",3,"BM",],
# ["BM3113",3,"BM",],
# ["BM4118",4,"BM",],
# ["BM4117",4,"BM",],
# ["BM4116",4,"BM",],
# ["BM4115",4,"BM",],
# ["BM4114",4,"BM",],
# ["BM4113",4,"BM",],
# ["BM5118",5,"BM",],
# ["BM5117",5,"BM",],
# ["BM5116",5,"BM",],
# ["BM5115",5,"BM",],
# ["BM5114",5,"BM",],
# ["BM5113",5,"BM",],
# ["BP1118",1,"BP",],
# ["BP1117",1,"BP",],
# ["BP1116",1,"BP",],
# ["BP1115",1,"BP",],
# ["BP1114",1,"BP",],
# ["BP1113",1,"BP",],
# ["BP2118",2,"BP",],
# ["BP2117",2,"BP",],
# ["BP2116",2,"BP",],
# ["BP2115",2,"BP",],
# ["BP2114",2,"BP",],
# ["BP2113",2,"BP",],
# ["BP3118",3,"BP",],
# ["BP3117",3,"BP",],
# ["BP3116",3,"BP",],
# ["BP3115",3,"BP",],
# ["BP3114",3,"BP",],
# ["BP3113",3,"BP",],
# ["BP4118",4,"BP",],
# ["BP4117",4,"BP",],
# ["BP4116",4,"BP",],
# ["BP4115",4,"BP",],
# ["BP4114",4,"BP",],
# ["BP4113",4,"BP",],
# ["BP5118",5,"BP",],
# ["BP5117",5,"BP",],
# ["BP5116",5,"BP",],
# ["BP5115",5,"BP",],
# ["BP5114",5,"BP",],
# ["BP5113",5,"BP",],
# ]

# for ri in rs:
#     r = Room(name=ri[0], floor=ri[1], building=ri[2])
#     try:
#         r.save()
#         print("Success!")
#     except peewee.IntegrityError:
#         pass

# b = Booking(who="David", when="2020-04-05", room=1)
# b.save()


r = Room.select()
print(len(r))

bb = Booking.select()
print(len(bb))
b = bb[0]
print(b.who, b.when, b.room.name)