#!/usr/bin/env python3
# NOTE: noinspection -> comments are only for Pycharm editor to comply with PEP8 regulations!

from tkinter import Frame, Label, Entry, StringVar
import setup as st
from CreateTable import Table
from UseCases import User, Driver, Booking, retrieve_driver_income

"""
Frame module for each user type.

Place:      University of Bedfordshire
Author:     Oszkar Feher
Date:       21 October 2020
"""


class BaseFrame(Frame):
    """BaseFrame class for all Frames.
    :inherit: Frame from tkinter"""
    def __init__(self, master=None):
        """Constructor"""
        # Call of constructor of parent class Frame.
        Frame.__init__(self, master)
        self.master = master
        self.config(bg=st.colors['bg'])
        self.build_grid()

    def build_grid(self):
        """Default grid layout for each Frame."""
        u, wc, wr = None, 1, 0
        self.grid_columnconfigure(0, weight=wc, uniform=u)
        self.grid_rowconfigure(0, weight=wr, uniform=u)


# noinspection PyPep8Naming
class User_Book(BaseFrame):
    """User_Book class for booking a trip by giving the distance.
    :inherit: BaseFrame"""
    def __init__(self, master=None):
        """Constructor"""
        # Call of constructor of parent class BaseFrame to overwrite
        BaseFrame.__init__(self, master)
        self.entry = None
        self.price = None

        self.build_labels()
        self.build_entry()

    def build_grid(self):
        """Grid builder which overwrites parent grid builder."""
        BaseFrame.build_grid(self)
        u, wc, wr = None, 1, 0
        for i in range(3):
            self.grid_columnconfigure(i, weight=wc, uniform=u)
        for r in range(5):
            self.grid_rowconfigure(r, weight=wr, uniform=u)

    def build_labels(self):
        """Label builder for <distance> Entry()"""
        labels = ['Distance (mile)', 'Price ($)']
        for i in range(len(labels)):
            Label(self, text=labels[i],
                  **st.login_label).grid(row=i+2, **st.login_label_g)
        self.price = Label(self, text=0, **st.price_label)
        self.price.grid(row=3, **st.price_label_g)

    def build_entry(self):
        """Entry builder for user distance input."""
        self.entry = Entry(self, **st.login_entry)
        self.entry.grid(row=2, **st.login_entry_g)


# noinspection PyPep8Naming
class User_Booking(BaseFrame):
    """User_Booking class to display trips in a table using Table() class.
    :inherit: BaseFrame"""
    def __init__(self, master=None):
        """Constructor"""
        # Call of constructor of parent class BaseFrame to overwrite
        BaseFrame.__init__(self, master)
        self.build_label()

    def build_grid(self):
        """Grid builder which overwrites parent grid builder."""
        BaseFrame.build_grid(self)
        u, wc, wr = None, 1, 0
        self.grid_columnconfigure(0, weight=wc, uniform=u)
        for i in range(6):
            self.grid_rowconfigure(i, weight=wr, uniform=u)

    def build_label(self):
        """Label builder for each trip table"""
        labels, row = ['Bookings', 'Due bookings', 'Past bookings'], 0
        for l in labels:
            Label(self, text=l, **st.booking).grid(row=row, **st.booking_g)
            row += 2

    @staticmethod
    def content(user_id, past: bool, flag: bool = False) -> tuple:
        """
        Static method used to create tables
        :param user_id: - user ID
        :param past: - boolean to select past trips
        :param flag: - boolean to change <fields>/column names
        :return: - tuple(), column names as <fields> and list of trips
        """
        # Column names for tables
        fields = ['Id', 'Booking dist.', 'Booking price',
                  'Driver name', 'Finished', 'Time of booking']
        # Selected columns from db
        columns = (Booking.id, Booking.distance, Booking.price,
                   Driver.first_name, Booking.past, Booking.time)
        # <where> conditions
        search = (Booking.user_id==user_id, Booking.past==past)
        # Default query
        query_set = Booking.select(*columns).join(Driver).where(*search).tuples()
        if flag:
            fields.remove("Driver name")
            fields[3] = "Confirmed"
            columns = (Booking.id, Booking.distance, Booking.price,
                       Booking.confirm, Booking.time)
            search = (Booking.user_id==user_id, Booking.confirm==past)
            query_set = Booking.select(*columns).where(*search).tuples()
        return fields, [item for item in query_set]

    def build_table(self, user_id=None):
        """<Bookings> table entries. All booked trips by current user."""
        fields, self.data = self.content(user_id, False, flag=True)
        self.table = Table(self, self.data, fields, 1, 0)

    def build_due_table(self, user_id=None):
        """<Due bookings> table entries. Confirmed trips by admin."""
        fields, self.due_data = self.content(user_id, False)
        self.due_table = Table(self, self.due_data, fields, 3, 0)

    def build_past_table(self, user_id=None):
        """<Past bookings> table entries. All trips which was confirmed by admin and finished by the driver."""
        fields, self.past_data = self.content(user_id, True)
        self.past_table = Table(self, self.past_data, fields, 5, 0)


# noinspection PyPep8Naming
class Driver_Booking(BaseFrame):
    """Driver_Booking class which display all trips allocated to a driver.
    :inherit: BaseFrame"""
    def build_grid(self):
        """Grid builder which overwrites parent grid builder."""
        BaseFrame.build_grid(self)
        u, wc, wr = None, 1, 0
        self.grid_columnconfigure(0, weight=wc, uniform=u)
        for i in range(2):
            self.grid_rowconfigure(i, weight=wr, uniform=u)

    def build_table(self, driver_id):
        """Table builder to display all trips allocated to a driver."""
        self.data, distance = [], []
        # Column names for table
        fields = ['Id', 'Client name', 'Tariff', 'Distance', 'Time of booking']
        # creating all booking data for table
        for item in Booking.select(Booking.id, User.first_name,
                                   Booking.price, Booking.distance,
                                   Booking.time).join(User).where(Booking.driver_id==driver_id,
                                                                  Booking.past==True).tuples():
            distance.append(item[3])
            self.data.append(item)
        self.table_past = Table(self, self.data, fields, 0, 0, size=True)
        # Displaying current driver income and distance driven.
        self.total = Label(self, text="Total income is: ${}    Total miles is: {}".format(
            retrieve_driver_income(driver_id)[0], sum(distance)),
                           **st.booking)
        self.total.grid(row=1, **st.booking_g)


# noinspection PyPep8Naming
class Admin_Use(BaseFrame):
    """Admin_Use class which display Bookings, User and Driver tables."""
    def build_booking_table(self):
        """Bookings table builder."""
        data = [i for i in Booking.select(Booking.id, User.first_name,
                                          Booking.confirm, Booking.past,
                                          Booking.time).join(User).tuples()]
        fields = ['Id', 'Client name', "Confirmed", 'Finished', 'Time of booking']
        self.table_booking = Table(self, data, fields, 0, 0, size=True)

    def build_user_table(self):
        """User table builder."""
        data = [i for i in User.select(User.id, User.first_name,
                                       User.last_name, User.spent,
                                       User.trips, User.joined_at).tuples()]
        fields = ['Id', 'First name', 'Last name', 'Total spent', 'Total trips', 'Joined at']
        self.table_user = Table(self, data, fields, 0, 0, size=True)

    def build_driver_table(self):
        """Driver table builder."""
        data = [i for i in Driver.select(Driver.id, Driver.first_name, Driver.last_name,
                                         Driver.distance, Driver.trips, Driver.income).tuples()]
        fields = ['Id', 'First name', 'Last name', 'Total miles', 'Total trips', 'Total income']
        self.table_driver = Table(self, data, fields, 0, 0, size=True)


class LogIn(BaseFrame):
    """LogIn class for log in input display.
    :inherit: BaseFrame"""
    def __init__(self, master=None):
        """Constructor"""
        # Call of constructor of parent class BaseFrame to overwrite
        BaseFrame.__init__(self, master)
        self.user = StringVar()
        self.user.set("User")

        self.entries = []

        self.build_labels()
        self.build_entry()

    def build_grid(self):
        """Grid builder which overwrites parent grid builder."""
        BaseFrame.build_grid(self)
        u, wc, wr = None, 1, 0
        for i in range(3):
            self.grid_columnconfigure(i, weight=wc, uniform=u)
        for r in range(5):
            self.grid_rowconfigure(r, weight=wr, uniform=u)

    def build_labels(self):
        """Log in labels builder."""
        welcome = Label(self, **st.welcome_label)
        welcome.grid(**st.welcome_g)

        labels = ['Username', 'Password']
        for i in range(len(labels)):
            Label(self, text=labels[i],
                  **st.login_label).grid(row=i+2, **st.login_label_g)

    def build_entry(self):
        """Log in input builder."""
        show = ""
        for i in range(2):
            if i == 1:
                show = "*"
            e = Entry(self, show=show, **st.login_entry)
            e.grid(row=2+i, **st.login_entry_g)
            self.entries.append(e)


class Register(BaseFrame):
    """Register class for registration input display.
    :inherit: BaseFrame"""
    user_type = None

    def __init__(self, master=None):
        """Constructor"""
        # Call of constructor of parent class BaseFrame to overwrite
        BaseFrame.__init__(self, master)
        self.user = StringVar()
        self.user.set("User")

        self.error_labels = []
        self.entries = []

        self.build_labels()
        self.build_entry()

    def build_grid(self):
        """Grid builder which overwrites parent grid builder."""
        BaseFrame.build_grid(self)
        u, wc, wr, r = None, 1, 0, 7
        if self.user_type == "driver":
            r = 8
        for i in range(3):
            self.columnconfigure(i, weight=wc, uniform=u)
        for i in range(r):
            self.rowconfigure(i, weight=wr, uniform=u)

    def build_labels(self):
        """Register input labels builder."""
        labels = st.reg_labels
        label_grid = st.reg_label_g
        err_grid = st.reg_err_g
        if self.user_type == 'driver':
            labels = st.reg_driver_labels
            label_grid = st.d_reg_label_g
            err_grid = st.d_reg_err_g
        for i in range(len(labels)):
            Label(self, text=labels[i], **st.reg_label).grid(row=i, **label_grid)
            if i < len(labels) - 1:
                err = Label(self, **st.reg_err)
                err.grid(row=i, **err_grid)
                self.error_labels.append(err)

    def build_entry(self):
        """Register input builder"""
        show, rows, r = "", [4, 5], 6
        entry_grid = st.reg_entry_g
        if self.user_type == 'driver':
            rows, r = [5, 6], 7
            entry_grid = st.d_reg_entry_g
        for i in range(r):
            if i in rows:
                # To hide password input
                show = "*"
            e = Entry(self, show=show, **st.login_entry)
            e.grid(row=i, **entry_grid)
            self.entries.append(e)


class DriverRegister(Register):
    """DriverRegister class for driver registration.
    It uses the Register class to add a registration input field for driver registration.
    :inherit: Register"""

    # Just user type is set to driver the rest remains the same as Registration class
    user_type = 'driver'

    def __init__(self, master=None):
        """Constructor"""
        # Call of constructor of parent class BaseFrame to overwrite
        Register.__init__(self, master)
