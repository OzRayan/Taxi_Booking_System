from UseCases import User, Driver, Admin

"""
This module is to populate the database if it's empty.
This has to run only if user types are needed.

Place:      University of Bedfordshire
Author:     Oszkar Feher
Date:       21 October 2020
"""


admin_data = {'first_name': 'Brother',
              'last_name': 'Big',
              'username': 'brother',
              'email': 'example@mail.com',
              'password': 'test'}

driver_data = [
    {'first_name': 'John',
     'last_name': 'Malvick',
     'username': 'john',
     'email': 'example@mail.com',
     'password': 'test',
     'reg_nr': 'HF32KOK'},
    {'first_name': 'Dave',
     'last_name': 'Malvick',
     'username': 'dave',
     'email': 'example2@mail.com',
     'password': 'test',
     'reg_nr': 'HF32TRD'},
    {'first_name': 'Jack',
     'last_name': 'Sparrow',
     'username': 'jack',
     'email': 'example3@mail.com',
     'password': 'test',
     'reg_nr': 'HT76YTR'},
    {'first_name': 'Mick',
     'last_name': 'Mock',
     'username': 'mick',
     'email': 'example4@mail.com',
     'password': 'test',
     'reg_nr': 'KU76YHN'},
    {'first_name': 'Bruce',
     'last_name': 'Wayne',
     'username': 'bruce',
     'email': 'example5@mail.com',
     'password': 'test',
     'reg_nr': 'BE78OBL'},
]

user_data = [
    {'first_name': 'Oscar',
     'last_name': 'White',
     'username': 'oscar',
     'email': 'example@mail.com',
     'password': 'test'},
    {'first_name': 'Rayan',
     'last_name': 'White',
     'username': 'rayan',
     'email': 'example2@mail.com',
     'password': 'test'},
    {'first_name': 'Karima',
     'last_name': 'White',
     'username': 'karima',
     'email': 'example3@mail.com',
     'password': 'test'},
    {'first_name': 'Karim',
     'last_name': 'Rayan',
     'username': 'karim',
     'email': 'example4@mail.com',
     'password': 'test'},
    {'first_name': 'Mehdi',
     'last_name': 'Rayan',
     'username': 'mehdi',
     'email': 'example5@mail.com',
     'password': 'test'},
]

Admin.create_user(**admin_data)
for i in user_data:
    User.create_user(**i)
for i in driver_data:
    Driver.create_user(**i)
