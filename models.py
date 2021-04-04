from peewee import *
from flask_login import UserMixin
from datetime import datetime, date, time

DATABASE = PostgresqlDatabase('dookies')

class Caretaker(UserMixin, Model):
    username = CharField(unique=True, null=False)
    email = CharField(unique=True, null=False)
    password = CharField(null=False)
    role = CharField(default='caretaker')
    created_at = DateTimeField(default= datetime.now)
    receive_emails = BooleanField(default=True)

    class Meta():
        database = DATABASE

class Dog(Model):
    name = CharField(null=False)
    birthday = DateField(default=date.today())
    breed = TextField()
    image = BlobField(null=True)
    notes = TextField()
    created_at = DateTimeField(default=datetime.now)

    class Meta():
        database = DATABASE

class Dog_Caretaker(Model):
    caretaker_id = ForeignKeyField(Caretaker)
    dog_id = ForeignKeyField(Dog)

    class Meta():
        database=DATABASE

class Vaccine(Model):
    vaccine_name = CharField(null=False)
    date_taken = DateField(default=date.today())
    dog_id = ForeignKeyField(Dog, backref='vaccines')
    created_at = DateTimeField(default= datetime.now)

    class Meta():
        database = DATABASE

class Medicine(Model):
    medicine_name = CharField(null=False)
    most_recent_date = DateField(default=date.today())
    frequency = TextField(default='1 per year')
    dog_id = ForeignKeyField(Dog, backref='medicines')
    created_at = DateTimeField(default= datetime.now)

    class Meta():
        database = DATABASE

class Dookie(Model):
    abnormal = BooleanField(null=False)
    food = TextField()
    color = TextField(default='brown')
    shape = TextField(default='log')
    consistency = TextField(default='compact')
    size = TextField(default='normal')
    content = TextField(default='nothing different')
    dog_id = ForeignKeyField(Dog, backref='dookies')
    created_at = DateTimeField(default= datetime.now)

    class Meta():
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Dog, Caretaker, Dog_Caretaker, Vaccine, Medicine, Dookie], safe=True)
    print('TABLES created')
    DATABASE.close()
