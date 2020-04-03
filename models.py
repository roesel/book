from peewee import IntegerField, CharField, TextField, BooleanField, ForeignKeyField, Model
from peewee import SqliteDatabase

db = SqliteDatabase('book.db')
db.connect()

class BaseModel(Model):
    class Meta:
        database = db

class Room(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(index=True, unique=True)
    floor = IntegerField()
    building = CharField()

class Booking(BaseModel):
    id = IntegerField(primary_key=True)
    who = CharField()
    when = CharField()
    room = ForeignKeyField(Room, to_field='id', related_name="room")

db.create_tables([Room, Booking])