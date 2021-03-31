from peewee import *
from flask_login import UserMixin
from datetime import datetime, date, time

DATABASE = PostgresqlDatabase('dookies')

class Caretaker(UserMixin, Model):
    username = CharField (unique=true, null=false)
    email = CharField
    password = CharField
    role = CharField
    created_at = DateTimeField

    class Meta():
        database = DATABASE
