import peewee
from app.models import Room, Booking, User
from playhouse.shortcuts import model_to_dict
from datetime import timedelta
from datetime import datetime

# APP safety settings
POP_LIMIT_ROOM = 1
POP_LIMIT_FLOOR = 3
POP_LIMIT_BUILDING = 5 

def get_all_rooms():
    rooms = Room.select() 
    return rooms

def create_booking(who, when, room_id):
    new_booking = Booking(who=who, when=when, room=room_id, status="pending")
    # new_booking = Booking(who=who, when=when, room=room_id)
    new_booking.save()
    return new_booking.id

def approve_booking(booking_id):
    requested_booking = Booking.get(booking_id=booking_id)
    requested_booking.status = 'approved'
    return True

def deny_booking(booking_id):
    requested_booking = Booking.get(booking_id=booking_id)
    requested_booking.status = 'denied'
    return True

def get_bookings_of_user(user_id):
    query = Booking.select().where(Booking.who==user_id)
    user_bookings = [model_to_dict(c) for c in query]
    return user_bookings

def get_bookings_of_room(room_name):
    query = Booking.select().join(Room).where(Room.name==room_name)
    room_bookings = [model_to_ict(c) for c in query]
    return room_bookings


def delete_booking(id):
    query = Booking.delete().where(Booking.id == id)
    num_of_deleted_rows = query.execute()
    return num_of_deleted_rows

def check_bookings_count(when, room_id):
    room_count = Booking.select().join(Room).where(
        (Booking.when == when) & 
        (Room.id == room_id)
    ).count()
    room_check = False
    if room_count < POP_LIMIT_ROOM:
        room_check = True

    room = Room.get(Room.id == room_id)
    floor_count = Booking.select().join(Room).where(
        (Booking.when == when) & 
        (Room.floor == room.floor) & 
        (Room.building  == room.building)
    ).count()
    floor_check = False
    if floor_count < POP_LIMIT_FLOOR:
        floor_check = True 

    building_count = Booking.select().join(Room).where( 
        (Booking.when == when) & 
        (Room.building  == room.building) 
    ).count()
    building_check = False
    if building_count < POP_LIMIT_BUILDING:
        building_check = True

    count_check = room_check*floor_check*building_check
    return count_check, [room_check, floor_check, building_check]

def check_create_booking(who, when, room_id):
    check_bookability, _ = check_bookings_count(when=when, room_id=room_id)
    if check_bookability == True:
        return create_booking(who=who, when=when, room_id=room_id) 
    else:
        return False

def get_free_slots(room_id, start_date, num_days):
    ''' Returns free slots for a room during the next 7 days. 
        : list of dicts
            : each item {when:date, available:t/f, reasons:list?]
    '''
    checks = []
    for i in range(num_days):
       when = start_date + timedelta(days=i)
       available, reasons = check_bookings_count(when.strftime("%Y-%m-%d"), room_id)
       checks.append({
           'when': when.strftime("%Y-%m-%d"),
           'available': bool(available),
           'reasons': reasons
        })

    return checks

def stats_occupation(when):
    floor_occupation = {}
    floor_occupation_rel = {}
    building_occupation = {}
    building_occupation_rel = {}
    rows = Room.select(Room.building).group_by(Room.building)
    buildings_of_the_campus = [row.building for row in rows]
    for building in buildings_of_the_campus:
        floor_occupation[building] = {}
        floor_occupation_rel[building] = {}
        rooms_of_the_building = Room.select().where(Room.building == building)
        rows = Room.select(Room.floor).where(Room.building == building).group_by(Room.floor)
        floors_of_the_building = [row.floor for row in rows]
        for floor in floors_of_the_building:
            floor_occupation[building][floor] = 0
            floor_occupation_rel[building][floor] = 0
    day_occupation = Booking.select().where(Booking.when == when)
    for booking in day_occupation:
        room_id = booking.room
        room = Room.get(Room.id == room_id)
        floor_occupation[room.building][room.floor] += 1
        floor_occupation_rel[room.building][room.floor] = floor_occupation[room.building][room.floor]/POP_LIMIT_FLOOR
    for building in floor_occupation:
            building_occupation[building] = sum(floor_occupation[building].values())
            building_occupation_rel[building] = building_occupation[building]/POP_LIMIT_BUILDING    
    return building_occupation, floor_occupation, building_occupation_rel, floor_occupation_rel


def stats_occupation_around(when, room_id):
    same_building_occupation = {}
    same_building_occupation_rel = {}
    same_floor_occupation = {}
    same_floor_occupation_rel = {}
    room = Room.get(Room.id == room_id)
    same_building_occupation = Booking.select().join(Room).where(Booking.when == when, Room.building == room.building).count()
    same_building_occupation_rel = same_building_occupation/POP_LIMIT_BUILDING
    same_floor_occupation = Booking.select().join(Room).where(Booking.when == when, Room.building == room.building, Room.floor == room.floor).count()
    same_floor_occupation_rel = same_floor_occupation/POP_LIMIT_FLOOR
    return same_building_occupation, same_floor_occupation, same_building_occupation_rel, same_floor_occupation_rel

def stats_for_plot_building(when):
    building_occupation, floor_occupation, building_occupation_rel, floor_occupation_rel = stats_occupation(when = when)
    plot_input = {}
    plot_input['labels'] = []
    plot_input['data'] = []
    plot_input['colors'] = []
    plot_input['text'] = 'Load of EPFL campus per building'
    plot_input['label'] = 'Rooms booked in this building'
    for b in building_occupation.keys():
        plot_input['labels'].append(b)
        plot_input['data'].append(building_occupation[b])
        if building_occupation_rel[b] < 1:
            plot_input['colors'].append('#007bff')
        else:
            plot_input['colors'].append('#dc3545')
    return plot_input


def prettify_date(date):
    """
    Input:
    ------
    `date`: str of form '%Y-%m-%d' ('2020-04-04')

    Returns:
    -------
    str of form '%B %d, %Y' ('April 4, 2020')
    """
    return datetime.strptime(date, '%Y-%m-%d').strftime('%B %d, %Y')



    
# --------- Debugging functions

def print_bookings():
    ''' Prints all bookings in terminal. '''
    q = Booking.select() 
    for b in q:
        print(b.id, b.who, b.when, b.room.name)

# This will only run if this .py script is directly executed
if __name__ == '__main__':
    a = check_create_booking('Maksim', '2020-04-06', 1)
    print(a)