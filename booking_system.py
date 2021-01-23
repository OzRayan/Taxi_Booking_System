#!/usr/bin/env python3
# NOTE: noinspection -> comments are only for Pycharm editor to comply with PEP8 regulations!

# Library imports
from datetime import datetime as dt
from datetime import timedelta as td
import random
# Used for password check
from werkzeug.security import check_password_hash
# Used to build main window and all widgets in the application
from tkinter import (Tk, Label, Button, Frame, StringVar, IntVar, BooleanVar,
                     DoubleVar, DISABLED, NORMAL, BOTH, Radiobutton)
from _tkinter import TclError
# Project imports
# Used for all string inputs, widget configurations, widget positioning, color and font setup
import setup as st
# All models (Use cases) for data manipulation:
# - creating models;
# - updating models;
# - deleting model instances.
# noinspection PyUnresolvedReferences
from UseCases import (User, Driver, Booking, Admin, user, user_by_id, update_user,
                      driver_by_id, driver, admin, create_booking, cancel_booking,
                      retrieve_booking_values, update_booking, update_booking_all,
                      retrieve_driver_count, retrieve_driver_id, update_driver,
                      update_driver_all, admin_delete_booking, admin_delete_driver,
                      admin_delete_user)
# Used for input values validation
from forms import UserForm, DriverForm

from info_screen import InfoScreen

from frames import (Admin_Use, Driver_Booking, User_Booking, User_Book,
                    LogIn, Register, DriverRegister)

"""
This application it's just for study purposes only and it's based on the university studies!
The application it's developed in tkinter GUI for better and easier user interaction 
of a fictional Taxi Booking system.
Before Login, user should select the type of user, by default is selected <User>,
If user doesn't exist, it will be prompted with an error message to select the correct user type.
User interaction:
    - as User:      - can register;
                    - after registration can login with the <username>;
                    - can book a trip by giving a distance in mile;
                    - after booking a trip, Admin must confirm the trip in order to assign a driver to the trip:
                        - <Confirmed> trip will be shown in a separate table;
                        - after confirmation, the selected trip will be shown in the <past bookings> table;
                        - trip can be canceled before confirmation, in this case trip will not be shown in the 
                        <past bookings> table.
                    - can logout.
                    
    - as Driver:    - can register;
                    - after registration can login with the <username>;
                    - view bookings where the current driver was allocated;
                    - can logout.
                    
    - as Admin:     - NOTE: admin CAN'T register just login if it was added previously in code level or shell!
                    - can login with <username>;
                    - can view all Users, Drivers and Bookings;
                    - can Confirm a trip;
                    - can view User and Driver details;
                    - can delete selected User, Driver or Booking one at the time;
                        NOTE: if User or Driver being deleted, the related bookings to the current user,
                         will be deleted as well!
                    - can logout.

Place:      University of Bedfordshire
Author:     Oszkar Feher
Date:       21 October 2020
"""


class TaxiBooking:
    """
    TaxiBooking class, main application class which will be called later on using TK() class.
    All main functionality it's built in this class.
    Further functionality is explained in each method accordingly.
    :methods: - __init__(master=root): - constructor, root=TK();
              - screen(): - sets main window size;
              - set_dimensions() -> tuple: - sets width, height and position of main window
                                            and returns a tuple of 4 values;
              - labels(): - user, driver labels definition;
              - variables(): - user id definition;
              - functions(): - user type buttons and button building functions definition/call;
              - build_frames(): - building all frames for buttons and tables;
              - build_grids(): - defining info and button frames grid;
              - show_frames(): brings upfront the desired frame for showing tables using .tkraise() function;
              - show_button_frames(): - brings upfront the desired frame for buttons using .tkraise() function;
              - build_info_labels(*args): - building all info labels, user-, driver-registered and available drivers.
                                     This is displayed on the top of the window with the clock and date;
              - build_error_label(*args): - building error label for later use, it's posioned under the buttons;
                       - build_signin_buttons(): - building main Login page buttons;
              - build_register_buttons(): - building Register page buttons;
              - build_radiobutton(): - building user type selection radio buttons;
              - build_user_buttons(): - building User page buttons;
              - build_driver_button(): - building Driver page button;
              - build_admin_buttons(): - building Admin page buttons;
              - wrapper(): - decorator for action_back() and action_signout() functions to clean entry fields and
                            error label;
              - set_command(text: str): - returns a function call for each button action or event;
              - set_user_buttons_state(text: str): - set all user buttons to original configuration;
              - setup_error_messages(dict_: dict, user_type: str): - sets error messages for register entry, User
                                                                    and Driver user types;
              - action_login(): - command for <Login> button;
              - action_register(): - command for main <Register> button;
              - action_signup(): - command for actual registration button;
              - action_radiobuttons(): - command for user type selection buttons;
              - action_back(): - decorated with wrapper(), command for <Back> button;
              - action_bookings(): - command for <Bookings> button for User;
              - action_booktrip(): - command for <Book trip> button for User;
              - action_confirmbooking(): - command for Creating a booking by the User;
              - action_canceltrip(): - command for <Cancel trip> button for User;
              - set_action_admin(text: str): - command for all admin buttons to desired state;
              - action_user(): - command for <User> button for Admin;
              - action_driver(): - command for <Driver> button for Admin;
              - action_booking(): - command for <Booking> button for Admin;
              - action_confirmtrip(): - command for <Confirm> button for Admin, assigning driver to Trip;
              - action_deletebooking(): - command for <Delete booking>, <Delete user> and <Delete driver>
                                        for Admin;
              - action_signout(): - decorated with wrapper(), command for <Signout> button for all user types;
              - user_booking_events(): - prepares User <Book trip> button when table row is selected;
              - user_confirm_events(): - prepares User <Confirm> button when table row is selected;
              - admin_confirm_booking_event(): - prepares Booking Id in case of Booking row selection;
              - set_admin_view_event(text: str): - prepares User, Driver or booking Id when table row is selected;
              - admin_view_user_event(): - calls set_admin_view_event() for User Id;
              - admin_view_driver_event(): - calls set_admin_view_event() for Driver Id;
              - set_admin_delete_event(text: str): - prepares User, Driver or Bookind Id to delete;
              - admin_delete_booking_event(): - prepares Admin <Delete booking> button when table row is selected;
              - admin_delete_user_event(): - prepares Admin <Delete user> button when table row is selected;
              - admin_delete_driver_event(): - prepares Admin <Delete driver> button when table row is selected;
              - update_trip_time(): - updates all Confirmed <Bookings> where was Driver assigned;
              - clear_signin_fields(): - deletes all signin input fields in case of Login, any user type;
              - clear_reg_fields(user_type: str): - deletes all registration input fields in case
                                                  of register User or Driver;
              - clear_distance_field(): - sets disitance and price to 0 for next Booking;
              - clear_reg_errors(user_type: str): - clear all error messages next to input fields;
              - check_password(user_type: str): - checks password with saved password for all user types;
              - update(): - updates all tables, User and Driver count, available Driver count, and time
                            every 1000 ms(1 second) using .after(<ms>, <update method>) method.
    """

    def __init__(self, master=None):
        """
        Constructor
        This method initializes the main frame with all table frames which is relevant after Login.
        :param: - master (root of Tk() )
        """
        # Main master root window
        self.master = master
        # Call of main window builder (size settings)
        self.screen()
        # Call of button and table frames builders
        self.build_frames()
        # Call of button and table frames grid builder
        self.build_grids()

        # Call of all user type labels builder
        self.labels()
        # Call of all user type variables builder
        self.variables()
        # Call of all button builders and button list builder
        self.functions()
        #
        # self.driver = None
        # self.booking = None

        # Call of error labels builder
        self.build_error_label()
        # Call of radio buttons (User type selection) builder
        self.build_radiobutton()

        # Call of update method which updates window in every 1000 ms (1 second)
        self.update()

    def screen(self):
        """Main window
        Minimal size 1024 / 600
        Set window geometry by calling set_dimensions() method
        """
        # Sets minimal window size of 1024 x 600
        self.master.minsize(1024, 600)
        # Sets desired window size
        self.master.geometry("{0}x{1}+{2}+{3}".format(*self.get_dimensions()))
        # Automatic master (root) update
        self.master.update_idletasks()

    def get_dimensions(self) -> tuple:
        """
        Set dimensions for master (root) window.
        :returns: - a tuple of dimensions
        """
        # Getting system screen width and height
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        # Setting master window size 65% of main screen width, 75% of main screen height
        width = screen_width // 100 * 65
        height = screen_height // 100 * 75
        # Setting master window position: half of main width/height - (minus) half of master window
        # width/height
        x = screen_width // 2 - width // 2
        y = screen_height // 2 - height // 2
        # Return a tuple of 4 dimension: width, height of master screen
        # and x, y vertical and horizontal position
        return width, height, x, y

    def labels(self):
        """Builds top info labels for time, registered User and Driver, available Drivers"""
        # Time text as string
        self.clock_text = StringVar()
        # Tracks build_info_labels() method for time update
        self.clock_text.trace("w", self.build_info_labels)

        # Registered user text as string
        self.user_label = StringVar()
        self.user_label.set("Users registered: ")
        # Registered user count as string
        self.user_nr = StringVar()

        # Registered driver text as string
        self.driver_label = StringVar()
        self.driver_label.set("Drivers registered: ")
        # Registered driver count as string
        self.driver_nr = StringVar()

        # Available driver text as string
        self.driver_av_label = StringVar()
        self.driver_av_label.set("Drivers available: ")
        # Available driver count as string
        self.driver_av_nr = StringVar()

    def variables(self):
        """Builds user type id variable"""
        # self.user_type = None
        # Frame name for registration
        self.action = st.action

        # Radio button position as integer, default=0 (User)
        self.var = IntVar()
        self.var.set(0)

        # User type Id as integer, default=0 (No user type)
        self.user_id = IntVar()
        self.user_id.set(0)

        # Used driver Id as integer, default=0, (No driver)
        # self.used_driver = IntVar()
        # self.used_driver.set(0)

        # Confirmation as boolean for booked trip, default=True
        self.confirmation = BooleanVar()
        self.confirmation.set(True)

        self.distance = DoubleVar()
        self.distance.set(0)

        self.price = DoubleVar()
        self.price.set(0)

        # Booking Id for admin action as integer, no default
        self.admin_booking_id = IntVar()

        # User Id for admin action as integer, no default
        self.admin_user_id = IntVar()

        # Driver Id for admin action as integer, no default
        self.admin_driver_id = IntVar()

    def functions(self):
        """Builds empty button lists and call of button builders"""
        # Sign in buttons empty list
        self.sign_in_buttons = []
        # Call of sign in buttons builder
        self.build_signin_buttons()

        # Register buttons empty list
        self.sign_up_button = []
        # Call of register buttons builder
        self.build_register_buttons()

        # User buttons empty list
        self.user_buttons = []
        # Call of User buttons builder
        self.build_user_buttons()

        # Driver button as None
        self.driver_button = None
        # Call of Driver button builder
        self.build_driver_button()

        # Admin buttons empty list
        self.admin_buttons = []
        # Call of Admin buttons builder
        self.build_admin_buttons()

    def build_frames(self):
        """Builds all frames and button frames"""
        # Main window frame with full fill
        self.main = Frame(self.master, bg=st.colors['bg'],
                          width=self.master.winfo_width(),
                          height=self.master.winfo_height())
        self.main.pack(fill=BOTH, expand=True)

        # Info frame to display time, registered users and drivers
        self.info_row = Frame(self.main, bg=st.colors['bg'])
        self.info_row.grid(**st.info_row_g)

        # Error frame under buttons frame to display all error or success messages
        self.error_row = Frame(self.main, bg=st.colors['bg'])
        self.error_row.grid(**st.error_row_g)

        # Button frames as empty dict
        self.button_frames = {}
        # Button frame names
        self.frame_names = st.frame_names
        # Populating button dict with all button frame names
        for name in self.frame_names:
            f = Frame(self.main, bg=st.colors['bg'])    # Creates for button set a frame
            self.button_frames[name] = f    # Adding frames to button dict
            f.grid(**st.f_g)
        # Show first button frame on front page
        self.show_button_frames("Login")

        # Frames empty dict for tables
        self.frames = {}
        # Populating frames dict with all displayed tables
        for f in (LogIn, Register, DriverRegister, User_Book,
                  User_Booking, Driver_Booking, Admin_Use):
            frame_name = f.__name__     # Getting table pages name by accessing the __name__ method
            frame = f(master=self.main)     # Initializing frames
            self.frames[frame_name] = frame     # Adding frames to frames dict
            frame.grid(**st.frame_g)
        # Show first frame on front page
        self.show_frames("LogIn")

    def build_grids(self):
        """Building all frames layout as a grid"""
        u = None
        # Main window 1 column
        self.main.grid_columnconfigure(0, weight=1, uniform=u)
        # Main window 4 row:
        #   - Info row
        #   - Buttons row
        #   - Error messages row
        #   - Tables row for each user type
        for i in range(4):
            self.main.grid_rowconfigure(i, weight=0, uniform=u)

        # Info row 4 columns:
        #   - Time column
        #   - User registered column
        #   - Driver registered column
        #   - Available drivers column
        for i in range(4):
            self.info_row.grid_columnconfigure(i, weight=1, uniform=u)
        # Info row 1 row
        self.info_row.grid_rowconfigure(0, weight=1, uniform=u)

        # Button row 5 columns for each user type
        column= 5
        for name in self.frame_names:
            if name == 'Admin_Use':
                column = 6
            for i in range(column):
                self.button_frames[name].grid_columnconfigure(i, weight=0, uniform=u)
            # Each button row has 1 row
            self.button_frames[name].grid_rowconfigure(0, weight=0, uniform=u)

    def show_frames(self, frame_name: str):
        """Brings to top the desired frame by the frame_name"""
        self.frames[frame_name].tkraise()

    def show_button_frames(self, frame_name: str):
        """Brings to top the desired button frame by the frame_name"""
        self.button_frames[frame_name].tkraise()

    # noinspection PyUnusedLocal
    def build_info_labels(self, *args):
        """
        Builds all labels for Info row
        :param args: - it's unused but for tk label construction an additional args it's necessary
                otherwise TypeError is raised. <*> - used if more than 1 parameter.
        """
        # Creating text for labels
        user_text = self.user_label.get() + self.user_nr.get()
        driver_text = self.driver_label.get() + self.driver_nr.get()
        driver_av_text = self.driver_av_label.get() + self.driver_av_nr.get()

        # Clock label added to Info row
        clock = Label(self.info_row, text=self.clock_text.get(), **st.login_label)
        clock.grid(**st.clock_g)
        # Registered User added to Info row
        user_label = Label(self.info_row, text=user_text, **st.login_label)
        user_label.grid(**st.user_label_g)
        # Registered Driver added to Info row
        driver_label = Label(self.info_row, text=driver_text, **st.login_label)
        driver_label.grid(**st.driver_label_g)
        # Available drivers added to Info row, <self> added to be able to call outside of this method
        self.driver_a_label = Label(self.info_row, text=driver_av_text, **st.login_label)
        self.driver_a_label.config(fg=st.colors['success'])     # Setting foreground color to green
        self.driver_a_label.grid(**st.driver_av_label_g)

    # noinspection PyUnusedLocal
    def build_error_label(self, *args):
        """
        Builds error label for all displayed error of succes messages.
        :param args: - it's unused but for tk label construction an additional args it's necessary
                otherwise TypeError is raised. <*> - used if more than 1 parameter.
        """
        self.error_label = Label(self.error_row, **st.error_label)
        self.error_label.grid(**st.error_label_g)

    # noinspection SpellCheckingInspection
    def build_signin_buttons(self):
        """
        Builds <Register> and <Login> buttons for <User> and <Driver> user type;
        <Login> for <Admin> user type.
        Buttons are used in main window which redirects for <Registration page>
        """
        labels = ["Register", "Log in"]
        for i in range(len(labels)):
            b = Button(self.button_frames['Login'], text="%s" % labels[i],
                       command=self.set_command(labels[i]), **st.sign_in_button)
            b.grid(column=i, **st.sign_in_g)
            self.sign_in_buttons.append(b)

    def build_register_buttons(self):
        """
        Builds <Register> and <Back> buttons for <User> and <Driver> user type.
        Actual Register or Sign Up action button.
        """
        labels = ["SignUp", "Back"]
        for label in labels:
            button = Button(self.button_frames['Register'],
                            text=label.replace("SignUp", "Register"),
                            command=self.set_command(label),
                            **st.reg_button)
            button.grid(column=labels.index(label), **st.reg_button_g)
            self.sign_up_button.append(button)

    def build_radiobutton(self):
        """
        Builds Radio buttons for user type selection.
        This is used for selecting the right Login or Registration user type:
        <User> <Driver> <Admin>. In case of <Admin>, registration is not available!
        """
        users = ["User", "Driver", "Admin"]
        for val, u in enumerate(users):
            Radiobutton(self.button_frames['Login'], text=u,
                        command=self.set_command('radiobuttons'),
                        value=val, variable=self.var,
                        **st.radio_button).grid(column=val+2, **st.radio_button_g)

    def build_user_buttons(self):
        """
        Builds <User> buttons inside User page.
        Sets button states.
        """
        # Button names/labels
        labels = ['Bookings', 'Book Trip', 'Confirm booking', 'Cancel Trip', 'Sign Out']
        for label in labels:
            # All buttons are disabled.
            button = Button(self.button_frames['User_Booking'],
                            text=label, state=DISABLED,
                            command=self.set_command(label.replace(' ', '').lower()),
                            **st.user_button)
            button.grid(column=labels.index(label), **st.user_button_g)
            self.user_buttons.append(button)
        # Enable <Bookings> and <Sign Out> buttons
        self.user_buttons[1]['state'] = NORMAL
        self.user_buttons[4]['state'] = NORMAL

    def build_driver_button(self):
        """
        Builds <Driver> button inside Driver page.
        Only <Sign Out> button is built.
        """
        self.driver_button = Button(self.button_frames['Driver_Booking'],
                                    text='Sign Out', state=NORMAL,
                                    command=self.set_command('signout'),
                                    **st.user_button)
        self.driver_button.grid(**st.driver_button_g)

    def build_admin_buttons(self):
        """
        Builds <Admin> buttons inside Admin page.
        Sets button states.
        """
        labels = ['Booking', 'User', 'Driver', 'Confirm trip', 'Delete booking', 'Sign Out']
        for label in labels:
            # All buttons are disabled.
            button = Button(self.button_frames['Admin_Use'],
                            text=label, state=DISABLED,
                            command=self.set_command(label.replace(' ', '').lower()),
                            **st.admin_button)
            button.grid(column=labels.index(label), **st.admin_button_g)
            self.admin_buttons.append(button)
        # Enables <User>, <Driver> and <Sign Out> buttons
        for i in [1, 2, 5]:
            self.admin_buttons[i]['state'] = NORMAL

    # noinspection PyMethodMayBeStatic
    def wrapper(self):
        """
        Decorative method for back() and signout() methods.
        Boths methods execute all the logic defined under inner() method.
        :return: - inner function without () call
        """
        def inner(inner_self):
            # Sets error message to empty string
            inner_self.error_label.config(text="")
            # Shows Login frame
            inner_self.show_frames('LogIn')
            # Shows Login button frame
            inner_self.show_button_frames("Login")
            # Sets radio button to User user type
            inner_self.var.set(0)
            # Sets price to 0
            inner_self.price.set(0)
            # Sets distance to 0
            inner_self.distance.set(0)
            # Sets Booking, User, Driver Id to 0
            inner_self.admin_booking_id.set(0)
            inner_self.admin_user_id.set(0)
            inner_self.admin_driver_id.set(0)
            # Clears all login fields
            inner_self.clear_signin_fields()
            # Clears all registration fields and error messages by calling the built-in eval(),
            # which evaluates whatever is in the string and calls is accordingly.
            for item in ['clear_reg_fields', 'clear_reg_errors']:
                eval(f"inner_self.{item}('user')")
                eval(f"inner_self.{item}('driver')")
        return inner

    # noinspection PyMethodMayBeStatic
    def set_command(self, text: str):
        """
        Sets a command for each button by calling eval() built-in method.
        If name (text) contains spacing, it replaces with nothing so the function names are called correctly.
        :param text: - button name which can contain spacing.
        :return: - a function call with corrected name (text) by taking out spacing and lowering it.
        """
        return eval(f"self.action_{text.replace(' ', '').lower()}")

    def set_user_buttons_state(self, text: str):
        """
        Sets all user buttons to desired state dependent by the <text> action.
        :param text: - action, if it's <action>, disables <Book trip> and <Cancel trip> buttons.
                        Sets <confirmation> to original state, True.
                     - action, if it's <init>, resets all user buttons to original state.
        """
        if text == 'action':
            self.user_buttons[2]['state'] = DISABLED
            self.user_buttons[3]['state'] = DISABLED
            self.user_buttons[2]['text'] = 'Book trip'  # If button name is <Confirm>, sets back to <Book trip>
            self.confirmation.set(True)
        if text == 'init':
            for i in range(5):
                if i == 1 or i == 4:    # Booking and Sign out buttons set to normal state
                    state = NORMAL
                else:
                    state = DISABLED    # Rest of the buttons set to disabled state
                self.user_buttons[i]['state'] = state

    def setup_error_messages(self, dict_: dict, user_type: str):
        """
        Sets error message for user input fields.
        :param dict_: - validator errors dictionary;
        :param user_type: - <User> or <Driver> user type
        """
        # <User> registration labels and frame
        labels, frame = st.err_labels, "Register"
        # If user type is <Driver>, set labels and frame for <Driver> user type
        if user_type == "driver":
            labels, frame = st.d_err_labels, "DriverRegister"
        for i in range(len(labels)):
            if labels[i] not in dict_:
                continue
            self.frames[frame].error_labels[i].config(text=dict_[labels[i]])

    def action_login(self):
        """
        Login button action.
        Check which user type is selected and give access to user accordingly.
        Sets user_id to user type Id.
        Shows the user type frames.
        """
        # Getting username and password input from login page
        username, password = (self.frames['LogIn'].entries[i].get() for i in range(2))

        values = {0: (user(username), None, "User_Booking"),
                  1: (driver(username), None, "Driver_Booking"),
                  2: (admin(username), None, "Admin_Use")}
        query, user_id, show_frame_up = values[self.var.get()]

        # Preparing message for no user
        message, fg = st.no_user, st.colors['error']
        if query.exists():      # Checks if user query exists
            # If exists, compares password with saved password
            if check_password_hash(query.first().password, password):
                # And sets message to success
                message, fg = st.login_success, st.colors['success']

                # Current user ID set()
                user_id = query.first().id
                # First frame after login depends on user type
                self.show_frames(show_frame_up)
                # Button array for user type
                self.show_button_frames(show_frame_up)
                # Sets buttons to initial
                self.set_user_buttons_state('init')
            else:
                # If password doesn't match, sets message to error
                message = st.login_error

        # Sets user type Id
        self.user_id.set(user_id)
        # Shows message as error or success
        self.error_label.config(text=message, fg=fg)

        # If not <Admin> is selected, build User or Driver table if exists
        try:
            if self.var.get() == 0:
                self.frames[show_frame_up].build_table(self.user_id.get())
                self.frames[show_frame_up].build_due_table(self.user_id.get())
                self.frames[show_frame_up].build_past_table(self.user_id.get())
            elif self.var.get() == 1:
                self.frames[show_frame_up].build_table(self.user_id.get())

            else:
                # If <Admin> is selected, build first available table, bookings
                self.frames[show_frame_up].build_booking_table()
        except TclError:
            pass

    def action_register(self):
        """Main register button action. Opens the Registration page"""
        # Shows user type registration page, User or Driver
        self.show_frames(self.action[self.var.get()])
        # Sets message to None
        self.error_label.config(text="")
        # Show registration button frame
        self.show_button_frames('Register')

    def action_signup(self):
        """
        Registration button action.
        Checks user type selection, User or Driver and validates input data.
        """
        # User type, validator form, registry frame
        user_type, validator, frame = 'user', UserForm(), "Register"
        # User type data, user type fields
        user_data, fields = User(), st.fields
        # If <Driver> is selected, all above variables are changed to Driver user type, default <User>
        if self.var.get() == 1:
            user_type, validator, frame = 'driver', DriverForm(), "DriverRegister"
            user_data, fields = Driver(), st.d_fields
        self.error_label.config(text="")    # Sets error message to None
        self.clear_reg_errors(user_type)     # Clears input fields error messages
        data = {}   # To be saved data empty dict
        # Loops through input fields and update data dictionary with input data
        entries = zip(range(len(self.frames[frame].entries)), fields)
        for index, d in entries:
            data.update({d: self.frames[frame].entries[index].get()})
        # Validates input values accordingly for each input field
        validator.validate(data)
        # If validation error message empty and passwords match, creates a user type model
        # for further use of the model exception message
        if len(validator.errors.values()) == 0 and self.check_password(user_type):
            u = user_data.create_user(**data)
            # If model creation exception message is None, model creation was successful and no exception
            # message is returned
            if u is None:
                # Sets error message to success
                self.error_label.config(text=st.reg_success, fg=st.colors['success'])
                self.clear_reg_fields(user_type)     # Clears input fields
                # Redirects to Login page and button frame
                self.show_frames('LogIn')
                self.show_button_frames("Login")
            else:
                # Else, show exception message, User already exists!
                self.error_label.config(text=u)
        # If validation fails, it will show all errors parallel with input field
        elif len(validator.errors.values()) != 0:
            self.setup_error_messages(validator.errors, user_type)

    # noinspection SpellCheckingInspection
    def action_radiobuttons(self):
        """
        User type selection action. Makes sure that if <Admin> is selected, <Register> button is disabled.
        Only <User> and <Driver> can register!
        """
        state = NORMAL
        if self.var.get() == 2:
            state = DISABLED
        self.sign_in_buttons[0].config(state=state)

    # noinspection PyArgumentList
    @wrapper
    def action_back(self):
        """
        <Back> button action decorated with wrapper() decorator function.
        All input fields, error messages, user type variables set to original state.
        """
        pass

    def action_bookings(self):
        """
        <Booking> button action. Brings on top the past bookins table and sets
        error message to None.
        Disables <Booking> and <Book trip> buttons and enables <Driver> button.
        :return:
        """
        self.show_frames('User_Booking')
        self.user_buttons[0]['state'] = DISABLED
        self.user_buttons[1]['state'] = NORMAL
        self.clear_distance_field()

        self.user_buttons[2]['state'] = DISABLED
        self.error_label.config(text='')

    # noinspection SpellCheckingInspection
    def action_booktrip(self):
        """
        User <Book trip> button command.
        """
        self.show_frames('User_Book')
        # Enables <Bookings> button
        self.user_buttons[0]['state'] = NORMAL
        # Disables <Book trip> button
        self.user_buttons[1]['state'] = DISABLED
        # Disables <Confirm booking> button
        self.user_buttons[2]['state'] = DISABLED
        self.error_label.config(text='')

    # noinspection SpellCheckingInspection
    def action_confirmbooking(self):
        """
        <Book trip> button action.
        Creates new booking or updates existing not confirmed booking.
        """
        create_booking(user_id=self.user_id.get(), distance=round(self.distance.get(), 2),
                       price=self.price.get())
        # Disables <Book trip> button
        self.user_buttons[2]['state'] = DISABLED
        # Sets confirmation to False
        self.confirmation.set(False)
        # Shows a success message
        self.error_label.config(text='Booking added', fg=st.colors['success'])
        # Build unconfirmed booking table
        self.frames["User_Booking"].build_table(self.user_id.get())
        self.clear_distance_field()

    # noinspection SpellCheckingInspection
    def action_canceltrip(self):
        """
        <Cancel trip> button action.
        Deletes booked trip which wasn't confirmed.
        """
        cancel_booking(self.admin_booking_id.get())
        # Sets buttons to original state and confirmation to True
        self.set_user_buttons_state('action')
        self.user_buttons[3]['state'] = DISABLED
        # Shows a success message
        self.error_label.config(text='Booking canceled', fg=st.colors['success'])
        # Updates available drivers table and bookings table
        self.frames["User_Booking"].build_table(self.user_id.get())

    def set_action_admin(self, text: str):
        """Sets <Admin> user buttons to initial state, builds <Admin> tables
        and changes <Delete --> button name for desired action.
        :param text: - <Delete --> button name (Delete user, Delete driver, Delete booking)
        """
        # Builds <Admin> table related to <text>
        eval(f'self.frames["Admin_Use"].build_{text}_table()')
        # Sets <Delete --> button to desired text
        self.admin_buttons[4]['text'] = f'Delete {text}'
        self.admin_buttons[3]['state'] = DISABLED
        self.admin_buttons[4]['state'] = DISABLED

        if text in ['driver', 'user']:
            self.admin_buttons[3]['text'] = f'View {text}'
        else:
            self.admin_buttons[3]['text'] = 'Confirm trip'

        query = eval(f"self.frames['Admin_Use'].table_{text}.table")
        query.selection_clear()

        for i in range(3):
            # If pushed button matches the <text>, disables button
            if self.admin_buttons[i]['text'] == text.capitalize():
                self.admin_buttons[i]['state'] = DISABLED
            # Else enables buttons
            else:
                self.admin_buttons[i]['state'] = NORMAL

    def action_user(self):
        """
        <User> admin button action.
        Calls set_action_admin() function with <user> name.
        """
        self.set_action_admin('user')

    def action_driver(self):
        """
        <Driver> admin button action.
        Calls set_action_admin() function with <driver> name.
        """
        self.set_action_admin('driver')

    def action_booking(self):
        """
        <Booking> admin button action.
        Calls set_action_admin() function with <booking> name.
        """
        self.set_action_admin('booking')

    # noinspection SpellCheckingInspection
    def action_confirmtrip(self):
        """
        Admin <Confirm trip> button.
        Updates Booking and driver and shows details of User or Drover.
        Another Tk() window is opened when button is pushed.
        """
        # If <Confirm trip> button == 'Confirm trip', allows to update Booking and Driver.
        if self.admin_buttons[3].cget('text') == 'Confirm trip':
            query = retrieve_driver_id()
            driver_id = random.choice([i[0] for i in query])
            update_booking(self.admin_booking_id.get(), driver_id, dt.now())
            update_driver(driver_id)
            self.frames['Admin_Use'].build_booking_table()
            self.admin_buttons[4]['state'] = DISABLED
        # If button == 'View user' or 'View driver', opens a Tk() window to display all details.
        if self.admin_buttons[3].cget('text') == 'View user':
            user_query = user_by_id(self.admin_user_id.get())
            user_fields = ('Id', 'First name', 'Last name', 'Username', 'Email',
                           'Total spent', 'Total trips', 'Joined at')
            InfoScreen(self.master, user_query, user_fields)

        if self.admin_buttons[3].cget('text') == 'View driver':
            driver_query = driver_by_id(self.admin_driver_id.get())
            driver_fields = ('Id', 'First name', 'Last name', 'Username', 'Email',
                             'Available', 'Car reg. nr.', 'Total income',
                             'Total trips', 'Total distance', 'Joined at')
            InfoScreen(self.master, driver_query, driver_fields)

    # noinspection SpellCheckingInspection
    def action_deletebooking(self):
        """
        <Delete --> admin button action.
        Deletes a model instance of User, Driver or Booking.
        """
        # Action for user type <User>
        action = self.admin_buttons[4].cget('text').split()[1]
        # Delete <User>, <Driver> or <Booking>
        eval(f"admin_delete_{action}(self.admin_{action}_id.get())")
        # Sets error message to success
        eval(f"self.error_label.config(text='{action.capitalize()} deleted!', fg=st.colors['success'])")
        # Updates table to display the correct row
        eval(f"self.master.after(50, self.frames['Admin_Use'].build_{action}_table())")
        # Changing the state of <Delete> button to DISABLED
        self.admin_buttons[4]['state'] = DISABLED

    # noinspection PyArgumentList
    # noinspection SpellCheckingInspection
    @wrapper
    def action_signout(self):
        """
        <Sign out> button action decorated with wrapper() decorator function.
        All input fields, error messages, user type variables set to original state.
        """
        # All user type variables are set to original state.
        self.error_label.config(text='Loged out', fg=st.colors['success'])
        self.user_id.set(0)
        # self.used_driver.set(0)
        self.confirmation.set(True)
        # Destroys all active tables.
        for k, v in st.dict_.items():
            eval(f'self.frames[{v}].build{k}_table().destroy()')
        self.frames["User_Booking"].build_table().destroy()

    def user_booking_events(self):
        """
        <User> user type <Book trip>/<Confirm> button event handler.
        It follows mouse event, checks if row is selected and updates button state.
        """
        entry = self.frames['User_Book'].entry.get()
        try:
            if float(entry) or int(entry):
                self.user_buttons[2]['state'] = NORMAL
                self.distance.set(self.frames['User_Book'].entry.get())
                self.price.set(round(int(self.distance.get()) * 2.23, 2))
                self.frames['User_Book'].price['text'] = self.price.get()
            else:
                self.user_buttons[2]['state'] = DISABLED
        except (TypeError, ValueError):
            self.frames['User_Book'].price['text'] = 'Just numbers!'

    def user_confirm_events(self):
        """
        <User> user type <Book trip>/<Confirm> button event handler.
        It follows mouse event, checks if row is selected and updates button state.
        """
        try:
            # Checks table selection and sets buttons state
            row_query = self.frames['User_Booking'].table.table
            if row_query.item(row_query.focus())['values']:
                self.admin_booking_id.set(row_query.item(row_query.focus())['values'][0])
                self.user_buttons[3]['state'] = NORMAL
            else:
                self.user_buttons[3]['state'] = DISABLED
        except AttributeError:
            pass

    def admin_confirm_booking_event(self):
        """
        Admin Bookings table listener. Sets Booking Id for later use.
        """
        try:
            # Checks table selection and sets buttons state
            row_query = self.frames['Admin_Use'].table_booking.table
            values = row_query.item(row_query.focus())['values']
            if values:
                # If there is available Drivers and Confirmed and Finished are False, sets Booking Id.
                if self.drivers > 0 and values[2] == "False" and values[3] == 'False':
                    self.admin_booking_id.set(values[0])
                    # Enables <Confirm trip> button
                    self.admin_buttons[3]['state'] = NORMAL
                else:
                    # Disables <Delete booking> button
                    self.admin_buttons[3]['state'] = DISABLED
        except AttributeError:
            pass

    def set_admin_view_event(self, text: str):
        """
        Admin view event listener. If a row is selected from User, Driver or Booking table,
        sets the Id for it.
        :param text: - user type text.
        """
        try:
            row_query = eval(f"self.frames['Admin_Use'].table_{text}.table")
            values = row_query.item(row_query.focus())['values']
            if values and self.admin_buttons[3]['text'].split()[1] == text:
                # print('Text: ', text)
                self.admin_buttons[3]['state'] = NORMAL
                eval(f"self.admin_{text}_id.set(row_query.item(row_query.focus())['values'][0])")
        except AttributeError:
            pass

    def admin_view_user_event(self):
        """
        User view event listener, calls set_admin_view_event().
        """
        self.set_admin_view_event('user')

    def admin_view_driver_event(self):
        """
        Driver view event listener, calls set_admin_view_event().
        """
        self.set_admin_view_event('driver')

    def set_admin_delete_event(self, text: str):
        """
        Admin delete event listener. If a row is selected from User, Driver or Booking table,
        sets the Id for it.
        :param text: - user type text.
        """
        try:
            state = DISABLED
            # selecting the right table by the 'text' user type
            row_query = eval(f"self.frames['Admin_Use'].table_{text}.table")
            values = row_query.item(row_query.focus())['values']
            # It checks if there is value/row selected from the table
            if values and self.admin_buttons[4]['text'].split()[1] == text:
                if text == 'booking':
                    # In case of Booking table, only not confirmed or past booking can be selected
                    if values[2] == 'False' or values[3] == 'True':
                        state = NORMAL
                else:
                    state = NORMAL
                # sets the button state depends on the selection
                self.admin_buttons[4]['state'] = state
                # sets user, driver or booking Id
                eval(f"self.admin_{text}_id.set(row_query.item(row_query.focus())['values'][0])")
        except AttributeError:
            pass

    def admin_delete_booking_event(self):
        """
        Admin booking delete event listener which calls set_admin_delete_event().
        """
        self.set_admin_delete_event('booking')

    def admin_delete_user_event(self):
        """
        Admin user delete event listener which calls set_admin_delete_event().
        """
        self.set_admin_delete_event('user')

    def admin_delete_driver_event(self):
        """
        Admin driver delete event listener which calls set_admin_delete_event().
        """
        self.set_admin_delete_event('driver')

    def update_trip_time(self):
        """Accepted trips update method for admin.
        It is called in update() to refresh tables every second.
        """
        # If Admin is logged in, all trips are retrieved
        if self.var.get() == 2:
            query = retrieve_booking_values()
            if query.exists():
                for item in query:
                    # If query exists, each row/entry/trip values are assigned to update
                    # trips, user spent, driver income and distance
                    book_id, driver_id, user_id, start_time, distance, price = item
                    # Tariff is calculated in average of 2.23/mile
                    if start_time + td(minutes=round(distance*2.23)) < dt.now():
                        self.error_label.config(text='Trip finished!', fg=st.colors['success'])
                        # Update trips which past the distance*1 mile price
                        update_booking_all(book_id)
                        # Updates assigned driver income and distance
                        update_driver_all(driver_id, round(price, 2), distance)
                        # Updates user spent
                        update_user(user_id, round(price, 2))
                        # Refreshes trips table
                        self.frames['Admin_Use'].build_booking_table()
                        # Sets <Booking>, <User>, <Driver> buttons to original state
                        self.admin_buttons[0]['state'] = DISABLED
                        self.admin_buttons[1]['state'] = NORMAL
                        self.admin_buttons[2]['state'] = NORMAL

    # noinspection SpellCheckingInspection
    def clear_signin_fields(self):
        """Clears sign in fields after log in and log out
        """
        for index in range(2):
            if index == 0:
                self.frames['LogIn'].entries[index].focus()
            self.frames['LogIn'].entries[index].delete(0, 'end')

    def clear_reg_fields(self, user_type: str):
        """Clears register fields for user or driver after registration.
        :param user_type: - user type for frame call."""
        frame = "Register"
        if user_type == "driver":
            frame = "DriverRegister"
        for index in range(len(self.frames[frame].entries)):
            if index == 0:
                self.frames[frame].entries[index].focus()
            self.frames[frame].entries[index].delete(0, 'end')

    def clear_distance_field(self):
        """Clears distance and price 'global' variables to 0.
        """
        self.frames['User_Book'].entry.delete(0, 'end')
        self.frames['User_Book'].price['text'] = ''
        self.distance.set(0)
        self.price.set(0)

    def clear_reg_errors(self, user_type: str):
        """
        Clears registration error messages for each attempt.
        :param user_type: - user type for frame call.
        """
        frame, r = "Register", 5
        if user_type == "driver":
            frame, r = "DriverRegister", 6
        for i in range(r):
            self.frames[frame].error_labels[i].config(text='')

    def check_password(self, user_type: str):
        """
        Password and check-password check. Makes sure that both passwords are the same
        in case of registration of user or driver.
        :param user_type: - user type for frame call.
        :returns: - boolean
        """
        frame = "Register"
        if user_type == "driver":
            frame = "DriverRegister"
        if self.frames[frame].entries[-1].get() != self.frames[frame].entries[-2].get():
            self.error_label.config(text=st.labels['password'])
            return False
        return True

    def update(self):
        """Master window refresh rate, 1000 ms (1 second)
        Updates all events/table row selection every second."""
        self.clock_text.set(f"{dt.now():%H:%M:%S    %a, %b %d %Y}")
        self.update_trip_time()
        self.user_booking_events()
        self.user_confirm_events()
        self.admin_confirm_booking_event()
        self.admin_view_user_event()
        self.admin_view_driver_event()
        self.admin_delete_booking_event()
        self.admin_delete_driver_event()
        self.admin_delete_user_event()
        # Retrieves all registered Users to display
        self.user_nr.set(User.select().count())
        # Retrieves all registered drivers to display
        self.driver_nr.set(Driver.select().count())
        # Retrieves all available drivers to display
        self.drivers = retrieve_driver_count()
        if self.drivers == 0:
            self.driver_a_label.config(fg=st.colors['error'])
        self.driver_av_nr.set(self.drivers)
        # Every 1 second or 1000 millisecond update() method is fed back to master.after() method
        self.master.after(1000, self.update)


if __name__ == '__main__':
    # Creating new TK()
    root = Tk()
    # Title of main window
    root.title('Taxi Booking System')
    # Icon of main window
    root.iconbitmap('Icon/icon_2.ico')
    # Main class call with newly created Tk() class
    TaxiBooking(root)
    # Tk() class loop to not crash
    root.mainloop()
