from tkinter import *

import setup as st


"""
This module is just for testing Table view. 

Place:      University of Bedfordshire
Author:     Oszkar Feher
Date:       21 October 2020
"""


class SimpleApp:

    def __init__(self, master=None):
        self.master = master
        x = int(float(65) * float(self.master.winfo_screenwidth()) / 100)
        y = int(float(75) * float(self.master.winfo_screenheight()) / 100)
        w = self.master.winfo_screenwidth() // 2 - x // 2
        h = self.master.winfo_screenheight() // 2 - y // 2
        self.master.geometry(f"{x}x{y}+{w}+{h}")
        self.master.update_idletasks()

        self.container = Frame(self.master, bg='red')
        self.container.pack(fill=BOTH, expand=True)

        self.container.grid_columnconfigure(0, weight=1, uniform=None)


        self.container.grid_rowconfigure(0, weight=0, uniform=None)
        self.container.grid_rowconfigure(1, weight=0, uniform=None)
        self.container.grid_rowconfigure(2, weight=0, uniform=None)
        self.container.grid_rowconfigure(3, weight=0, uniform=None)
        self.container.grid_rowconfigure(4, weight=0, uniform=None)
        # self.container.grid_rowconfigure(1, weight=0, uniform=None)
        # self.container.grid_rowconfigure(2, weight=1, uniform=None)

        # self.first_frame = Frame(self.container, bg='green')
        # # self.first_frame.pack(fill=BOTH, expand=True)
        # self.first_frame.grid(row=0, column=0, sticky='news', rowspan=1)
        #

        # self.second_frame = Frame(self.container, bg='blue')
        # # self.second_frame.pack(fill=BOTH, expand=True)
        # self.second_frame.grid(row=1, column=0, sticky='news', padx=0, pady=10)

        from CreateTable import Table
        from UseCases import User as U
        from UseCases import Driver as D
        from UseCases import Booking as B
        from UseCases import Admin as A
        # from UseCases import delete_booking
        # U.delete().where(U.id==4).execute()
        # B.delete().execute()
        # B.update(driver_id=1).where(B.user_id==1).execute()
        # D.update(available=True).where((D.available==False)).execute()
        import datetime
        list_ = [i for i in U.select(U.id, U.first_name, U.last_name, U.username, U.email).tuples()]
        list_2 = [i for i in D.select(D.id, D.reg_nr, D.available, D.first_name, D.last_name,
                                      D.username, D.email).tuples()]
        list_3 = [i for i in B.select().tuples()]

        list_4 = [i for i in B.select(B.id, B.time,
                                      B.confirm, B.user_id,
                                      B.driver_id).tuples()]
        # list_4 = [i for i in list_4.tuples()]  datetime.datetime.strptime(str(B.time), "%Y-%m-%d_%H:%M")
        list_5 = [i for i in A.select().tuples()]
        no_fields = ['password', 'joined_at', 'is_admin']
        # print(D._meta.fields.keys())
        # fields = []
        fields = ['Id', "Booking time", "Confirm", "User name", "Driver name"]
        # noinspection PyProtectedMember
        for i in B._meta.fields.keys():
            if i not in no_fields:
                fields.append(i.replace('_', ' ').capitalize())
        # fields = [i.replace('_', " ").capitalize() for i in U._meta.fields.keys() if i not in no_fields]
        # print(((B._meta.fields.keys())))
        # print(fields)
        # print(list_3)
        # B.delete().execute()
        print(list_4)

        l = Table(self.container, list_4, fields, 0, 0)

        item = l.table.focus()
        # print(l.table.identify)

        self.button = Button(self.container,
                             bg='white',
                             text="Print List Item",
                             command=lambda:print(l.table.item(l.table.focus())['values'][0]))
        self.button.grid(row=1, column=0, sticky='news', rowspan=1)

        # def delete():
        #     delete_user(user_id=l.tv.item(l.tv.focus())['values'][0])
        #     l.tv.delete(l.tv.selection()[0])
        self.delete = Button(self.container,
                             bg='white',
                             text="Delete Item",
                             command=lambda: (delete_user(user_id=l.table.item(l.table.focus())['values'][0]),
                                              l.table.delete(l.table.selection()[0])))
        self.delete.grid(row=2, column=0, sticky='news', rowspan=1)


if __name__ == "__main__":
    root = Tk()
    SimpleApp(root)
    root.mainloop()