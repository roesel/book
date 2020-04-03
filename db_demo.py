import peewee
from models import Room, Booking

print("\n")
print("Printing all rooms in BM on floor 4:")
rooms = Room.select().where((Room.building == "BM") & (Room.floor == 4))
for r in rooms:
    print(r.name)

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