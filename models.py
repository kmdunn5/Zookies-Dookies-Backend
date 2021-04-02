from peewee import *
from flask_login import UserMixin
from datetime import datetime, date, time

DATABASE = PostgresqlDatabase('dookies')

class Caretaker(UserMixin, Model):
    username = CharField(unique=true, null=false)
    email = CharField(unique=true, null=false)
    password = CharField(null=false)
    role = CharField(default='caretaker')
    created_at = DateTimeField(default= datetime.now)

    class Meta():
        database = DATABASE

class Dog(Model):
    name = CharField(null=False)
    birthday = DateField(default=date.today())
    breed = CharField
    image = BlobField
    caretaker = ForeignKeyField(Caretaker, backref='dogs')
    notes = TextField

    class Meta():
        database = DATABASE


class Vaccines(Model):
    vaccine_name = CharField(null=False)
    date_taken = DateField(default=date.today())
    dog_id = ForeignKeyField(Dogs, backref='vaccines')

    class Meta():
        database = DATABASE

class Medicines(Model):
    medicine_name = CharField(null=False)
    most_recent_date = DateField(default=date.today())
    frequency = TextField(default='1 per year')
    dog_id = ForeignKeyField(Dogs, backref='medicines')

    class Meta():
        database = DATABASE

class Dookies(Model):
    abnormal = BooleanField(null=False)
    color = TextField(default='brown')
    shape = TextField(default='log')
    consistency = TextField(default='compact')
    size = TextField(default='normal')
    consistency = TextField(default='nothing different')

    class Meta():
        database = DATABASE
