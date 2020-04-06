import peewee
from app.models import Room, Booking
from playhouse.shortcuts import model_to_dict

def get_accessible_rooms(user_id):
    if user_id == 2:
        rooms = Room.select().where(Room.name << ['BM4118', 'BM5117', 'BM4113'])
    elif user_id == 3:
        rooms = Room.select().where(Room.name << ['BM4118', 'BM4114', 'SV1115', 'SV2116'])
    elif user_id == 4:
        rooms = Room.select().where(Room.name << ['CH1117', 'CH3117', 'CH3118', 'BM4113', 'SV2116'])
    else:
        rooms = Room.select()

    room_list = [model_to_dict(c) for c in rooms]
    return room_list

# This will only run if this .py script is directly executed
if __name__ == '__main__':
    a = get_accessible_rooms(2)
    print(a)