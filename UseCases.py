#!/usr/bin/env python3
# NOTE: noinspection -> comments are only for Pycharm editor to comply with PEP8 regulations!

import datetime

from peewee import *
from werkzeug.security import generate_password_hash


"""
This module use peewee ORM (Object Relational Mapper) and werkzeug libraries.

Place:      University of Bedfordshire
Author:     Oszkar Feher
Date:       21 October 2020
"""

# Database
db = SqliteDatabase("records.db")


class BaseModel(Model):
    """BaseModel class to utilize database <db> by giving the Meta data.
    :inherit: - Model from peewee."""
    class Meta:
        database = db


class Abstract(BaseModel):
    """
    Abstract class. A base class for all models with base fields.
    All fields are mandatory.
    :inherit: - BaseModel.
    """
    first_name = CharField(null=False, max_length=40)
    last_name = CharField(null=False, max_length=40)
    # unique - makes sure that repeated user names are not accepted
    username = CharField(null=False, unique=True, max_length=40)
    password = CharField(null=False, max_length=40)
    # unique - makes sure that repeated emails are not accepted
    email = CharField(null=False, unique=True, max_length=40)
    joined_at = DateTimeField(default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    is_admin = BooleanField(default=False)


class User(Abstract):
    """
    User class with additional fields for User type.
    :inherit: - Abstract.
    :methods: - create_user class method.
    """
    spent = FloatField(default=0)
    trips = IntegerField(default=0)

    # noinspection PyShadowingNames
    @classmethod
    def create_user(cls, first_name, last_name, username,
                    email, password, admin=False):
        """
        Creates a customer/user.

        :param first_name: - string.
        :param last_name: - string.
        :param username: - string, must be unique.
        :param email: - string, must be unique.
        :param password: - string, password is saved as a hashed string not the actual password.
        :param admin: - boolean, user not admin so it's false.
        :return: - string if user already exists with same username or email.
        """
        try:
            # Makes sure that all fields are given and than it can save it.
            # If input fields are just half given, entry will not be saved and protects the database from
            # incomplete input.
            with db.transaction():
                cls.create(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=admin
                )
        except IntegrityError:
            return "User already exists!"


class Driver(Abstract):
    """
    Driver class with additional fields for Driver type.
    :inherit: - Abstract.
    :methods: - create_user class method.
    """
    reg_nr = CharField(null=False, max_length=10)
    available = BooleanField(default=True)
    income = FloatField(default=0)
    trips = IntegerField(default=0)
    distance = FloatField(default=0)

    # noinspection PyShadowingNames
    @classmethod
    def create_user(cls, first_name, last_name, username,
                    email, password, reg_nr, admin=False):
        """
        Creates a driver.

        :param first_name: - string.
        :param last_name: - string.
        :param username: - string, must be unique.
        :param email: - string, must be unique.
        :param password: - string, password is saved as a hashed string not the actual password.
        :param reg_nr: - string.
        :param admin: - boolean, user not admin so it's false.
        :return: - string if driver already exists with same username or email.
        """
        try:
            # Makes sure that all fields are given and than it can save it.
            # If input fields are just half given, entry will not be saved and protects the database from
            # incomplete input.
            with db.transaction():
                cls.create(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    reg_nr=reg_nr,
                    is_admin=admin
                )
        except IntegrityError:
            return "Driver already exists!"


class Booking(BaseModel):
    """Booking class for trips booking.
    :inherit: - BaseModel
    """
    user_id = ForeignKeyField(User)
    driver_id = ForeignKeyField(Driver, null=True, default=None)
    distance = FloatField()
    price = FloatField()
    confirm = BooleanField(default=False)
    past = BooleanField(default=False)
    confirm_at = DateTimeField(null=True, default=None)
    time = DateTimeField(default=datetime.datetime.now().strftime("%Y-%m-%d...%H:%M"))


class Admin(Abstract):
    """
    Admin class..
    :inherit: - Abstract.
    :methods: - create_user class method.
    """
    # noinspection PyShadowingNames
    @classmethod
    def create_user(cls, first_name, last_name, username,
                    email, password, admin=True):
        """
        Creates an admin.

        :param first_name: - string.
        :param last_name: - string.
        :param username: - string, must be unique.
        :param email: - string, must be unique.
        :param password: - string, password is saved as a hashed string not the actual password.
        :param admin: - boolean.
        :return: - string if admin already exists with same username or email.
        """
        try:
            # Makes sure that all fields are given and than it can save it.
            # If input fields are just half given, entry will not be saved and protects the database from
            # incomplete input.
            with db.transaction():
                cls.create(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=admin
                )
        except IntegrityError:
            return "Admin already exists!"


def user(username):
    """
    Retrieves user by username.
    :param username: - string, User username.
    :return: - query.
    """
    return User().select().where(User.username==username)


def user_by_id(user_id):
    """
    Retrieves user by ID.
    :param user_id: - integer, User ID.
    :return: - tuple of fields.
    """
    return User().select(User.id, User.first_name,
                         User.last_name, User.username,
                         User.email, User.spent, User.trips,
                         User.joined_at).where(User.id==user_id).tuples()


def update_user(user_id, price):
    """
    Updates User trips and spent fields.
    :param user_id: - integer, User ID.
    :param price: - float, payed amount for a trip.
    """
    User.update(trips=User.trips+1,
                spent=User.spent+price).where(User.id==user_id).execute()


def driver_by_id(driver_id):
    """
    Retrieves driver by ID.
    :param driver_id: - integer, Driver ID.
    :return: - tuple of fields.
    """
    return Driver().select(Driver.id, Driver.first_name,
                           Driver.last_name, Driver.username,
                           Driver.email, Driver.available,
                           Driver.reg_nr, Driver.income,
                           Driver.trips, Driver.distance,
                           Driver.joined_at).where(Driver.id==driver_id).tuples()


def driver(username):
    """
    Retrieves driver by username.
    :param username: - string, Driver username.
    :return: - query.
    """
    return Driver().select().where(Driver.username==username)


def admin(username):
    """
    Retrieves admin by username.
    :param username: - string, Admin username.
    :return: - query.
    """
    return Admin().select().where(Admin.username==username)


def create_booking(user_id, distance, price):
    """
    Creates a trip for User by giving distance and price of the trip.
    :param user_id: - integer, User ID.
    :param distance: - float, given by the current user in mile.
    :param price: - float, distance multiplied with 2.23 (2.23 / mile).
    """
    Booking.create(user_id=user_id, distance=distance, price=price)


def cancel_booking(booking_id):
    """
    Deletes a trip by Booking ID.
    :param booking_id: - integer, the trip ID.
    """
    Booking.select().where(Booking.id==booking_id).first().delete_instance()


def retrieve_booking_values():
    """
    Retrieves trips what is confirmed by Admin but not finished by the Driver.
    :return: - tuple of trips.
    """
    return Booking.select(Booking.id,
                          Booking.driver_id,
                          Booking.user_id,
                          Booking.confirm_at,
                          Booking.distance,
                          Booking.price).where(Booking.confirm==True,
                                               Booking.past==False).tuples()


def update_booking(booking_id, driver_id, confirm_at):
    """
    Updates a booking by ID. When Admin allocates a driver to the booked trip.
    :param booking_id: - integer, trip ID.
    :param driver_id: - integer, Driver ID allocated to this trip.
    :param confirm_at: - datetime, the time when it was confirmed.
    """
    Booking.update(confirm=True,
                   driver_id=driver_id,
                   confirm_at=confirm_at).where(Booking.id==booking_id).execute()


def update_booking_all(booking_id):
    """
    Updates trip which are finished by the Driver.
    :param booking_id: - integer, Booking ID.
    """
    Booking.update(past=True).where(Booking.id==booking_id).execute()


def retrieve_driver_count():
    """
    Retrieves Drivers count. All Driver which are available.
    :return: - integer, all available Drivers.
    """
    return Driver.select().where(Driver.available==True).count()


def retrieve_driver_id():
    """
    Retrieves Drivers ID which are available.
    :return: - tuple of Driver IDs.
    """
    return Driver.select(Driver.id).where(Driver.available==True).tuples()


def retrieve_driver_income(driver_id):
    """
    Retrieves one Driver income by Driver ID.
    :param driver_id: - integer, Driver ID.
    :return: - tuple of income of one Driver.
    """
    return Driver.select(Driver.income).where(Driver.id==driver_id).tuples().first()


def update_driver(driver_id):
    """
    Updates Driver by ID. Allocated Driver to a trip.
    :param driver_id: - integer, Driver ID.
    """
    Driver.update(available=False).where(Driver.id==driver_id).execute()


def update_driver_all(driver_id, income, distance):
    """
    Updates all Drivers by ID. Updates availability, total income, total distance driven and total trips
    made by the Driver.
    :param driver_id: - integer, Driver ID.
    :param income: - float, one trip price.
    :param distance: - float, one trip diatance.
    """
    Driver.update(available=True, income=Driver.income+income,
                  distance=Driver.distance+distance,
                  trips=Driver.trips+1).where(Driver.id==driver_id).execute()


def admin_delete_booking(booking_id):
    """
    Deletes a trip by Booking ID.
    :param booking_id: - integer, Booking ID.
    """
    Booking.select().where(Booking.id==booking_id).first().delete_instance()


def admin_delete_user(user_id):
    """
    Deletes User by ID. Only Admin can delete User.
    :param user_id: - integer, User ID.
    """
    # First is deleted the user
    User.select().where(User.id==user_id).first().delete_instance()
    # The User related trips are selected by User ID
    booking = Booking.get_or_none(Booking.user_id==user_id)
    # If trips exists for this User, it is deleted as well.
    try:
        if booking is not None:
            booking.first().delete_instance()
    except AttributeError:
        pass


def admin_delete_driver(driver_id):
    """
    Deletes Driver by ID. Only Admin can delete a Driver.
    :param driver_id: - integer, Driver ID.
    """
    Driver.select().where(Driver.id==driver_id).first().delete_instance()


# Connecting to database
db.connect()
# Creating tables if doesn't exists by <safe> set to True
db.create_tables([User, Driver, Booking, Admin], safe=True)
# Close database
db.close()

print(Admin().select().where(Admin.username==1))
