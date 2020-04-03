import peewee
from models import Room, Booking

def create_booking(who, when, where):
    new_booking = Booking(who=who, where=where, when=when)
    new_booking.save()
    return new_booking.id

def get_bookings_of_user(user_name):
    user_bookings = Booking.select().where(Booking.who==user_name)
    return user_bookings

def get_bookings_of_room(room_name):
    room_bookings = Booking.select().join(Room).where(Room.name==room_name)
    return room_bookings

def delete_booking(id):
    query = Booking.delete().where(Booking.id == id)
    num_of_deleted_rows = query.execute()
    return num_of_deleted_rows