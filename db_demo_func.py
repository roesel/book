import peewee
from models import Room, Booking
from playhouse.shortcuts import model_to_dict

def create_booking(who, when, where):
    new_booking = Booking(who=who, where=where, when=when)
    new_booking.save()
    return new_booking.id

def get_bookings_of_user(user_name):
    query = Booking.select().where(Booking.who==user_name)
    user_bookings = [model_to_dict(c) for c in query]
    return user_bookings

def get_bookings_of_room(room_name):
    query = Booking.select().join(Room).where(Room.name==room_name)
    room_bookings = [model_to_dict(c) for c in query]
    return room_bookings

def delete_booking(id):
    query = Booking.delete().where(Booking.id == id)
    num_of_deleted_rows = query.execute()
    return num_of_deleted_rows

# --------- Debugging functions

def print_bookings():
    ''' Prints all bookings in terminal. '''
    q = Booking.select() 
    for b in q:
        print(b.id, b.who, b.room.name)
