from app import login

from peewee import IntegerField, CharField, TextField, BooleanField, ForeignKeyField, Model
from peewee import SqliteDatabase

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SqliteDatabase('book.db')
db.connect()

class BaseModel(Model):
    class Meta:
        database = db

class User(UserMixin, BaseModel):
    id = IntegerField(primary_key=True)
    email = CharField(index=True, unique=True)
    name = CharField(index=True)
    password_hash = CharField()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Room(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(index=True, unique=True)
    floor = IntegerField()
    building = CharField()

class Booking(BaseModel):
    id = IntegerField(primary_key=True)
    when = CharField()
    who = ForeignKeyField(User, to_field='id', related_name="user")
    room = ForeignKeyField(Room, to_field='id', related_name="room")

db.create_tables([Room, Booking, User])

@login.user_loader
def load_user(id):
    return User.select().where(User.id==int(id)).get()