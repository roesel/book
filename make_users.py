import peewee
from app.models import User

users = [
    {"name":"David R.", "email":"david.roesel@epfl.ch", "password-plain":"horsefish"},
    {"name":"Maksim E.", "email":"maksim.eremchev@epfl.ch", "password-plain":"catmouse"},
    {"name":"Olesia A.", "email":"olesia.altunina@epfl.ch", "password-plain":"ponydog"},
    {"name":"Serhii K.", "email":"sergey.kulik@epfl.ch", "password-plain":"birdsnake"},
]

for user in users:
    u = User.create(name=user["name"], email=user["email"], password_hash="placeholder")
    u.set_password(user["password-plain"])
    u.save()