#!/usr/bin/env python3
# NOTE: noinspection -> comments are only for Pycharm editor to comply with PEP8 regulations!

# noinspection PyProtectedMember
from peewee_validates import (Validator, StringField, validate_not_empty,
                              validate_email)

"""
This module is contains all validation forms for user and driver registration.

Place:      University of Bedfordshire
Author:     Oszkar Feher
Date:       21 October 2020
"""


class BaseForm(Validator):
    """BaseForm class for input validation. It makes sure that input fields are not empty
    and the email is a valid email.
    :inherit: Validator from peewee_validates"""
    first_name = StringField(required=True, max_length=40,
                             validators=[validate_not_empty()])
    last_name = StringField(required=True, max_length=40,
                            validators=[validate_not_empty()])
    username = StringField(required=True, max_length=40,
                           validators=[validate_not_empty()])
    email = StringField(required=True, max_length=40,
                        validators=[validate_not_empty(), validate_email()])
    password = StringField(required=True, max_length=40,
                           validators=[validate_not_empty()])


class UserForm(BaseForm):
    """UserForm class for user registration input validation.
    This class use the BaseForm class
    :inherit: BaseForm
    """
    pass


class DriverForm(BaseForm):
    """DriverForm class for driver registration input validation.
    This class use the BaseForm class.
    Added field for registration number.
    :inherit: BaseForm
    """
    reg_nr = StringField(required=True, max_length=40,
                         validators=[validate_not_empty()])
