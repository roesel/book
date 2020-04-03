import peewee
from models import Room, Booking

def get_bookings_of_room(room_name)
    #print("\n")
    #print("Printing all rooms in BM on floor 4:")
    rooms = Booking.select().where((Booking.name == room_name) & (Room.floor == 4))
    for r in rooms:
        print(r.name)
    return booikng_id, who, when

def create_booking(who, when, where):
    new_id = len(Booking) + 1
    Booking[new_id].who = who
    Booking[new_id].when = when
    Booking[new_id].where = where
    return True


print('\n')
print('Printing all bookings (with room name!):')
bookings = Booking.select()
print("{} bookings found.".format(len(bookings)))
for b in bookings:
    print(b.who, b.when, b.room.name)

# print('\n')
# print('Making a new booking:')
# new_booking = Booking(who="Serhii", when="2020-04-07", room=2)
# try:
#     new_booking.save()
# except:
#     print("Something went wrong with making new booking.")
#     raise

# print('\n')
# print('Deleting all bookings by Serhii:')
# query = Booking.delete().where(Booking.who=="Serhii")
# query.execute()