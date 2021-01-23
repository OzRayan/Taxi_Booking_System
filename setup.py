#!/usr/bin/env python3

from collections import OrderedDict
from tkinter import NORMAL, CENTER, SUNKEN, LEFT


"""
This module contains all the settings for main window, frames, grids and frame names.

Place:      University of Bedfordshire
Author:     Oszkar Feher
Date:       21 October 2020
"""

# All the fonts user for the application
fonts = OrderedDict([
    ("buttons", ("Helvetica", 12, 'bold')),
    ("combo", ("Helvetica", 12, "bold")),
    ("table", ("Helvetica", 12, "bold")),
    ("heading", ("Helvetica", 14, "bold")),
    ("label", ("Times New Roman", 16)),
    ("mini_info", ("Times New Roman", 18, 'bold')),
    ("info", ("Helvetica", 13)),
    ("welcome", ("Times New Roman", 26, "bold")),
])

# Labels to be displayed in different part of the application
labels = OrderedDict([
    ("welcome", "Welcome to Taxi Booking System"),
    ("req", "* Required fields"),
    ("password", "Make sure passwords are matching!")
])

# All the colours used for the app
colors = OrderedDict([
    ('bg', '#F4E5B3'),
    ('fg', '#454238'),
    ('info', 'white'),
    ('clock', '#020202'),
    ('entry', '#DCEBE5'),
    ('button', '#DFB269'),
    ('button_d', '#020202'),
    ('button_af', '#F4E5B3'),
    ('button_ab', '#93B3A6'),
    ('error', '#CD422A'),
    ('table', '#FAF4E1'),
    ('success', '#48A54D'),

])

# Messages
login_error = "Username or password incorrect. Make sure you selected the right user type!"

no_user = "User doesn't exist!. Make sure you selected the right user type!"

login_success = "Login successful!"

reg_success = "You have registered successfully!"

# Frame names as list or dictionary
action = {0: "Register", 1: "DriverRegister"}

dict_ = {'': 'User_Driver', '_past': 'User_Booking', '_booking': 'Admin_Use',
         '_user': 'Admin_Use', '_driver': 'Admin_Use'}

reg_labels = ['First Name', 'Last Name', 'Username',
              'Email', 'Password', 'Check-password']

reg_driver_labels = ['First Name', 'Last Name', 'Username',
                     'Email', 'Registration nr.', 'Password',
                     'Check-password']

err_labels = ["first_name", "last_name", "username", "email", "password"]

d_err_labels = ["first_name", "last_name", "username", "email", "reg_nr", "password"]

fields = ['first_name', 'last_name', 'username', 'email', 'password']

d_fields = ['first_name', 'last_name', 'username', 'email', 'reg_nr', 'password']

frame_names = ("Login", "Register", "User_Booking", "Driver_Booking", "Admin_Use")

# Registration label conf.
reg_label = {"font": fonts['label'],
             'bg': colors['bg'],
             'fg': colors['fg']}

# Registration error label conf.
reg_err = {'text': '',
           'font': fonts['label'],
           'bg': colors['bg'],
           'fg': 'red'}

# Welcome label conf.
welcome_label = {'text': labels['welcome'],
                 'font': fonts['welcome'],
                 'bg': colors['bg'],
                 'fg': colors['fg']}

# Log in input conf.
login_entry = {"font": fonts['label'],
               'bg': colors['entry'],
               'fg': colors['fg'],
               'bd': 2,
               'width': 25}

# Log in label conf.
login_label = {'font': fonts['label'],
               'bg': colors['bg'],
               'fg': colors['fg']}

# Driver price label conf.
price_label = {'font': fonts['label'],
               'bg': colors['bg'],
               'fg': colors['fg'],
               'bd': 1,
               'width': 10}

# Info screen label conf.
mini_label = {'bg': colors['bg'],
              'fg': colors['fg'],
              'justify': LEFT,
              'font': fonts['mini_info']}

# Booking/trips conf.
booking = {'font': fonts['label'],
           'bg': colors['bg'],
           'fg': colors['fg']}

# Info screen conf.
mini_frame = {'bg': colors['bg'],
              'highlightbackground': colors['fg'],
              'highlightcolor': colors['fg'],
              'highlightthickness': 3}

# Radio buttons conf. (User type selection buttons)
radio_button = {'font': fonts['buttons'],
                'bg': colors['bg'],
                'fg': colors['fg'],
                'activebackground': colors['entry'],
                'selectcolor': colors['entry'],
                'width': 20,
                'bd': 2,
                'indicatoron': 0}

# Registration button conf.
reg_button = {'font': fonts['buttons'],
              'anchor': CENTER,
              'bg': colors['button'],
              'state': NORMAL,
              'fg': colors['fg'],
              'overrelief': SUNKEN,
              'activebackground': colors['button_ab'],
              'activeforeground': colors['button_af'],
              'width': 20,
              'bd': 2,
              'disabledforeground': colors['info']}

# User button conf.
user_button = {'font': fonts['buttons'],
               'anchor': CENTER,
               'bg': colors['button'],
               'fg': colors['fg'],
               'overrelief': SUNKEN,
               'activebackground': colors['button_ab'],
               'activeforeground': colors['button_af'],
               'width': 16,
               'bd': 2,
               'disabledforeground': colors['info']}

# Admin button conf.
admin_button = {'font': fonts['buttons'],
                'anchor': CENTER,
                'bg': colors['button'],
                'fg': colors['fg'],
                'overrelief': SUNKEN,
                'activebackground': colors['button_ab'],
                'activeforeground': colors['button_af'],
                'width': 14,
                'bd': 2,
                'disabledforeground': colors['info']}

# Log in button conf. (after adding credentials)
sign_in_button = {'font': fonts['buttons'],
                  'anchor': CENTER,
                  'bg': colors['button'],
                  'state': NORMAL,
                  'fg': colors['fg'],
                  'overrelief': SUNKEN,
                  'activebackground': colors['button_ab'],
                  'activeforeground': colors['button_af'],
                  'width': 10,
                  'bd': 2,
                  'disabledforeground': colors['info']}

# Ok button conf. of the info screen
mini_button = {'bg': colors['button'],
               'fg': colors['fg'],
               'font': fonts['buttons'],
               'activeforeground': colors['button_af'],
               'activebackground': colors['button_ab'],
               'width': 5}

# Error message label conf.
error_label = {'text': '',
               'font': fonts['label'],
               'bg': colors['bg'],
               'fg': colors['error']}

# Registration label position
reg_label_g = {'column': 0, 'sticky': 'ns', 'padx': 5, 'pady': 25}
# Driver registration label position
d_reg_label_g = {'column': 0, 'sticky': 'ns', 'padx': 5, 'pady': 20}
# Registration error label position
reg_err_g = {'column': 2, 'sticky': 'nws', 'padx': 5, 'pady': 25}
# Driver registration error label position
d_reg_err_g = {'column': 2, 'sticky': 'nws', 'padx': 5, 'pady': 20}
# Registration input position
reg_entry_g = {'column': 1, 'sticky': 'nws', 'padx': 0, 'pady': 25}
# Driver registration input position
d_reg_entry_g = {'column': 1, 'sticky': 'nws', 'padx': 0, 'pady': 20}
# Log in input position
login_entry_g = {'column': 1, 'sticky': 'ns', 'padx': 0, 'pady': 30, 'columnspan': 1}
# Welcome label position
welcome_g = {'row': 0, 'column': 0, 'sticky': 'ns', 'padx': 30, 'pady': 30, 'columnspan': 3}
# Log in label position
login_label_g = {'column': 0, 'sticky': 'nes', 'padx': 5, 'pady': 35}
# Radio button/user type buttons position
radio_button_g = {'row': 0, 'sticky': 'nes', 'padx': 0, 'pady': 15}
# Registration button position for User and Driver
reg_button_g = {'row': 0, 'sticky': 'nes', 'padx': 15, 'pady': 15}
# User button position
user_button_g = {'row': 0, 'sticky': 'news', 'padx': 15, 'pady': 10}
# Admin button position
admin_button_g = {'row': 0, 'sticky': 'news', 'padx': 10, 'pady': 10}
# Driver button position
driver_button_g = {'row': 0, 'column': 0, 'sticky': 'news', 'padx': 15, 'pady': 10}
# Main window info row position
info_row_g = {'row': 0, 'column': 0, 'sticky': 'news', 'padx': 0, 'pady': 0}
# Mina window error row position
error_row_g = {'row': 2, 'column': 0, 'sticky': 'news', 'padx': 0, 'pady': 0}
# Button row frame position
f_g = {'row': 1, 'column': 0, 'sticky': 'news', 'padx': 0, 'pady': 0}
# Frames position for each user type
frame_g = {'row': 3, 'column': 0, 'sticky': 'news', 'padx': 0, 'pady': 0}
# Time label position
clock_g = {'row': 0, 'column': 0, 'sticky': 'w', 'padx': 10, 'pady': 0}
# Registered User label position
user_label_g = {'row': 0, 'column': 1, 'sticky': 'news', 'padx': 0, 'pady': 0}
# Registered Drivers label position
driver_label_g = {'row': 0, 'column': 2, 'sticky': 'e', 'padx': 10, 'pady': 0}
# Available Drivers label position
driver_av_label_g = {'row': 0, 'column': 3, 'sticky': 'e', 'padx': 10, 'pady': 0}
# Info row label position
error_label_g = {'row': 0, 'column': 2, 'sticky': 'nes', 'padx': 10, 'pady': 0}
# Login (after input) position
sign_in_g = {'row': 0, 'sticky': 'new', 'padx': 15, 'pady': 15}
# Table names label position
booking_g = {'column': 0, 'sticky': 'nws', 'padx': 15, 'pady': 8}
# Trip price label position
price_label_g = {'column': 1, 'sticky': 'ns', 'padx': 0, 'pady': 35, 'columnspan': 1}
