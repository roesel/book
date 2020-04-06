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
    requested_booking = Booking.get(id=booking_id)
    requested_booking.status = 'approved'
    requested_booking.save()
    return True

def get_booking_text(booking_id):
    booking = Booking.get(id=booking_id)
    user_name = User.get(id=booking.who).name
    date = prettify_when(booking.when)
    room = Room.get(id=booking.room).name
    return [room, date, user_name]

def deny_booking(booking_id):
    requested_booking = Booking.get(id=booking_id)
    requested_booking.status = 'denied'
    requested_booking.save()
    return True

def get_bookings_of_user(user_id):
    query = Booking.select().where(Booking.who == user_id)
    user_bookings = [model_to_dict(c) for c in query]
    for b in user_bookings:
        booking = Booking.get(Booking.id == b['id'])
        room = Room.get(Room.id == booking.room)
        same_floor_occupation = Booking.select().join(Room).where(Booking.when == booking.when, Room.building == room.building, Room.floor == room.floor).count()
        same_floor_occupation_rel = same_floor_occupation/POP_LIMIT_FLOOR*100
        b['value_abs'] = same_floor_occupation
        b['value_rel'] = same_floor_occupation_rel
    return user_bookings

def get_bookings_of_user_old(user_id):
    query = Booking.select().where(Booking.who == user_id)
    user_bookings = [model_to_dict(c) for c in query]
    return user_bookings

def get_bookings_of_room(room_name):
    query = Booking.select().join(Room).where(Room.name == room_name)
    room_bookings = [model_to_dict(c) for c in query]
    return room_bookings

def get_pending_bookings_new(sort_by='booking_id'):
    query = Booking.select().where(Booking.status == 'pending')
    if sort_by == 'when':
        query_sorted = query.order_by(Booking.when)
    else:
        query_sorted = query
    pending_bookings = [model_to_dict(c) for c in query_sorted]
    for b in pending_bookings:
        booking = Booking.get(Booking.id == b['id'])
        same_room_pending = Booking.select().join(Room).where(Booking.when == booking.when, Booking.status == 'pending', Room.id == booking.room).count()
        if same_room_pending == 1:
            b['unique_request'] = True
        else:
            b['unique_request'] = False
    return pending_bookings

def get_pending_bookings(sort_by='booking_id'):
    query = Booking.select().where(Booking.status == 'pending')
    if sort_by == 'when':
        query_sorted = query.order_by(Booking.when)
    else:
        query_sorted = query
    pending_bookings = [model_to_dict(c) for c in query_sorted]
    return pending_bookings

def delete_booking(id):
    query = Booking.delete().where(Booking.id == id)
    num_of_deleted_rows = query.execute()
    return num_of_deleted_rows

def check_bookings_count(when, room_id, status='approved'):
    assert status in ['approved', 'pending', 'denied']
    room_count = Booking.select().join(Room).where(
        (Booking.when == when) & 
        (Room.id == room_id) &
        (Booking.status == status)
    ).count()
    room_check = False
    if room_count < POP_LIMIT_ROOM:
        room_check = True

    room = Room.get(Room.id == room_id)
    floor_count = Booking.select().join(Room).where(
        (Booking.when == when) & 
        (Room.floor == room.floor) & 
        (Room.building == room.building) &
        (Booking.status == status)
    ).count()
    floor_check = False
    if floor_count < POP_LIMIT_FLOOR:
        floor_check = True 

    building_count = Booking.select().join(Room).where( 
        (Booking.when == when) & 
        (Room.building == room.building) &
        (Booking.status == status)
    ).count()
    building_check = False
    if building_count < POP_LIMIT_BUILDING:
        building_check = True

    count_check = room_check * floor_check * building_check
    return bool(count_check), [room_check, floor_check, building_check]

def check_create_booking(who, when, room_id):
    check_bookability, _ = check_bookings_count(when=when, room_id=room_id)
    if check_bookability == True:
        return create_booking(who=who, when=when, room_id=room_id) 
    else:
        return False

def get_floor_count(when, room_id, status='approved'):
    assert status in ['approved', 'pending', 'denied']
    room = Room.get(Room.id == room_id)
    floor_count = Booking.select().join(Room).where(
        (Booking.when == when) & 
        (Room.floor == room.floor) & 
        (Room.building == room.building) &
        (Booking.status == status)
    ).count()

    return floor_count

def check_bookings_of_user_room_when(user_id, room_id, when, status='approved'):
    assert status in ['approved', 'pending', 'denied']
    # print(when)
    # print(status)
    # print('user_id', user_id)
    # print('room_id', room_id)
    query = Booking.select().join(Room).where(
        (Booking.who == user_id) &
        (Room.id == room_id) &
        (Booking.when == when) &
        (Booking.status == status))
    count = query.count()
    # print(count)
    # if count > 0:
    #     print('peow')
    #     print(query[0].status)
    assert count in [0, 1]
    return bool(count)

def count_to_int(count, max_count=POP_LIMIT_FLOOR, num_int=2):
            step = float(max_count) / num_int
            for i in range(num_int - 1):
                if i <= count < i + step:
                    return num_int - i
            if max_count - step <= count <= max_count:
                return 1
            else:
                return None

def get_free_slots_for_user(user_id, room_id, start_date, num_days):
    ''' Returns free slots for a room during the next 7 days. 
        : list of dicts
            : each item {when:date, available:t/f, reasons:list?]
    '''
    checks = []
    for i in range(num_days):
        when = start_date + timedelta(days=i)

        approved = {}
        approved['AM'] = check_bookings_of_user_room_when(
            user_id, room_id, when.strftime("%Y-%m-%d") + '-AM', status='approved')
        approved['PM'] = check_bookings_of_user_room_when(
            user_id, room_id, when.strftime("%Y-%m-%d") + '-PM', status='approved')

        pending = {}
        pending['AM'] = check_bookings_of_user_room_when(
            user_id, room_id, when.strftime("%Y-%m-%d") + '-AM', status='pending')
        pending['PM'] = check_bookings_of_user_room_when(
            user_id, room_id, when.strftime("%Y-%m-%d") + '-PM', status='pending')

        available, reasons = {}, {}
        available['AM'], reasons['AM'] = check_bookings_count(when.strftime("%Y-%m-%d") + '-AM', room_id)
        available['PM'], reasons['PM'] = check_bookings_count(when.strftime("%Y-%m-%d") + '-PM', room_id)

        floor_count = {}
        floor_count['AM'] = get_floor_count(
            when.strftime("%Y-%m-%d") + '-AM', room_id, status='approved')
        floor_count['PM'] = get_floor_count(
            when.strftime("%Y-%m-%d") + '-PM', room_id, status='approved')

        floor_count['AM'] = count_to_int(floor_count['AM'])
        floor_count['PM'] = count_to_int(floor_count['PM'])

        code = {}
        for k in ['AM', 'PM']:
            if approved[k]:
                code[k] = -1
            elif pending[k]:
                code[k] = -2
            elif available[k]:
                code[k] = floor_count[k]
            elif not available[k]:
                code[k] = 0
            else:
                code[k] = -1000
            
        checks.append({
            'when': when.strftime("%Y-%m-%d"),
            'code': [code['AM'], code['PM']],
            'available': [available['AM'], available['PM']],
            'approved': [approved['AM'], approved['PM']],
            'pending': [pending['AM'], pending['PM']],
            'reasons': [reasons['AM'], reasons['PM']]
            })

    return checks

def get_limits():
    limits = {'building':POP_LIMIT_BUILDING, 'floor':POP_LIMIT_FLOOR, 'room':POP_LIMIT_ROOM}
    return limits

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
    day_occupation = Booking.select().where(Booking.when == when, Booking.status == 'approved')
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

def stats_for_plot_buildings(when_day):
    plot_input = {}
    plot_input['labels'] = []
    plot_input['data_AM'] = []
    plot_input['colors_AM'] = []
    plot_input['label_AM'] = 'Morning'
    plot_input['data_PM'] = []
    plot_input['colors_PM'] = []
    plot_input['label_PM'] = 'Evening'
    plot_input['text'] = 'Load of EPFL campus by buildings'
    plot_input['under_text'] = 'Building'
    building_occupation_AM, floor_occupation_AM, building_occupation_rel_AM, floor_occupation_rel_AM = stats_occupation(when = when_day + '-AM')
    building_occupation_PM, floor_occupation_PM, building_occupation_rel_PM, floor_occupation_rel_PM = stats_occupation(when = when_day + '-PM')
    for b in building_occupation_AM.keys():
        plot_input['labels'].append(b)
        plot_input['data_AM'].append(building_occupation_AM[b])
        plot_input['data_PM'].append(building_occupation_PM[b])
        if building_occupation_rel_AM[b] < 1:
            plot_input['colors_AM'].append('#3395ff')
        else:
            plot_input['colors_AM'].append('#dc3545')
        if building_occupation_rel_PM[b] < 1:
            plot_input['colors_PM'].append('#0062cc')
        else:
            plot_input['colors_PM'].append('#dc3545')
    return plot_input

def stats_for_plot_time(building, month):
    plot_input = {}
    plot_input['labels'] = []
    plot_input['data_AM'] = []
    plot_input['colors_AM'] = []
    plot_input['label_AM'] = 'Morning'
    plot_input['data_PM'] = []
    plot_input['colors_PM'] = []
    plot_input['label_PM'] = 'Evening'
    plot_input['text'] = 'Load of the building during the month'
    plot_input['under_text'] = 'Day'
    plot_input['label'] = 'Rooms booked in this building'
    for day in range(30):
        day_string = '2020-{:02d}-{:02d}'.format(month,day+1)
        print(day_string)
        plot_input['labels'].append('{:d}'.format(day+1))
        building_occupation_AM, floor_occupation_AM, building_occupation_rel_AM, floor_occupation_rel_AM = stats_occupation(when = day_string + '-AM')
        plot_input['data_AM'].append(building_occupation_AM[building])
        if building_occupation_rel_AM[building] < 1:
            plot_input['colors_AM'].append('#3395ff')
        else:
            plot_input['colors_AM'].append('#dc3545')
        building_occupation_PM, floor_occupation_PM, building_occupation_rel_PM, floor_occupation_rel_PM = stats_occupation(when = day_string + '-PM')
        plot_input['data_PM'].append(building_occupation_PM[building])
        if building_occupation_rel_PM[building] < 1:
            plot_input['colors_PM'].append('#0062cc')
        else:
            plot_input['colors_PM'].append('#dc3545')
    return plot_input

def stats_for_plot_time_floor(building, floor, month):
    plot_input = {}
    plot_input['labels'] = []
    plot_input['data_AM'] = []
    plot_input['colors_AM'] = []
    plot_input['label_AM'] = 'Morning'
    plot_input['data_PM'] = []
    plot_input['colors_PM'] = []
    plot_input['label_PM'] = 'Evening'
    plot_input['text'] = 'Load of {:01d} floor during the month'.format(floor)
    plot_input['under_text'] = 'Day'
    plot_input['label'] = 'Rooms booked on {:01d} floor'.format(floor)
    for day in range(30):
        day_string = '2020-{:02d}-{:02d}'.format(month,day+1)
        plot_input['labels'].append('{:d}'.format(day+1))
        building_occupation_AM, floor_occupation_AM, building_occupation_rel_AM, floor_occupation_rel_AM = stats_occupation(when = day_string + '-AM')        
        plot_input['data_AM'].append(floor_occupation_AM[building][floor])
        if floor_occupation_rel_AM[building][floor] < 1:
            plot_input['colors_AM'].append('#3395ff')
        else:
            plot_input['colors_AM'].append('#dc3545')
        building_occupation_PM, floor_occupation_PM, building_occupation_rel_PM, floor_occupation_rel_PM = stats_occupation(when = day_string + '-PM')
        plot_input['data_PM'].append(floor_occupation_PM[building][floor])
        if floor_occupation_rel_PM[building][floor] < 1:
            plot_input['colors_PM'].append('#0062cc')
        else:
            plot_input['colors_PM'].append('#dc3545')
    return plot_input

def stats_for_plot_time_floors(building, month):
    plot_input_pack = []
    rows = Room.select(Room.floor).where(Room.building == building).group_by(Room.floor)
    floors_of_the_building = [row.floor for row in rows]
    for floor in floors_of_the_building:
        stats_for_plot_time_floor(building = building, floor = floor, month = month)
        plot_input_pack.append(stats_for_plot_time_floor(building = building, floor = floor, month = month))
    return plot_input_pack

def list_buildings():
    rows = Room.select(Room.building).group_by(Room.building)
    buildings_of_the_campus = [row.building for row in rows]
    return buildings_of_the_campus

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

def prettify_when(when):
    date = '-'.join(when.split('-')[0:3])
    return prettify_date(date)+" "+when.split('-')[-1]

    
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