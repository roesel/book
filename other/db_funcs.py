import peewee
from models import Room, Booking
from playhouse.shortcuts import model_to_dict

from db_demo_func import *

def get_free_slots(room_id):
    ''' Returns free slots for a room during the next N days. 
        : list of dicts
            : each item {when:date, available:t/f, reasons:list?]
    '''
    next_n_days = ["2020-04-{:02d}".format(x) for x in range(5, 5+7)]
    print(next_n_days)
    out = []
    for day in next_n_days:
        available, reasons = check_bookings_count(day, room_id)
        out.append( {'when':day, 'available':bool(available), 'reasons':reasons} )
    return out


print_bookings()

print(get_free_slots(1))
#print("Query returned {} rows.".format(len(q)))

