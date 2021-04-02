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
    name = CharField
    birthday = DateField(default=date.today())
    age = IntegerField(default=0)
    caretaker = ForeignKeyField(Caretaker, backref='dogs')
    core_vaccines = ForeignKeyField(Vaccines, backref='dogs')

class Vaccines(Model):
    vaccine_name = CharField
    date_taken = DateField
    core = BooleanField

class Medicines(Model):
    



class Dookies(Model):
    abnormal = BooleanField(null=False)
    color = CharField(default='brown')
    shape = CharField(default='log')
    consistency = CharField(default='compact')
    size = CharField(default='normal')
    consistency = CharField(default='nothing different')

