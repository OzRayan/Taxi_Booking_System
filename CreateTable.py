#!/usr/bin/env python3

from tkinter.ttk import Treeview, Style, Scrollbar

import setup as st


"""
This module is to create tables to display using Treeview from tkinter.ttk.

Place:      University of Bedfordshire
Author:     Oszkar Feher
Date:       21 October 2020
"""


class Table:
    """Table class used to display a table with database rows."""
    def __init__(self, root, lst: list, fields: list, row: int, column: int, size=False):
        """
        Constructor.
        :param root: - the frame where it will be displayed the table.
        :param lst: - list of rows from database.
        :param fields: - column names.
        :param row: - integer, to position table on Frame grid.
        :param column: - integer, to position table on Frame grid.
        :param size: - boolean, to define height of the table. If no rows to display,
                        height is 0 else height is 20 rows. Default 4 rows.
        """
        col, height = tuple([i for i in range(len(fields))]), 4
        if len(lst) < 1:
            height = 0
        if size:
            height = 20
        # Style for the treeview
        self.style = Style()
        # Modify the font of the body
        self.style.configure("Treeview", highlightthickness=3, bd=3, background=st.colors['table'],
                             font=st.fonts['table'])
        # Modify the font of the headings
        self.style.configure("Treeview.Heading", font=st.fonts['heading'])
        # Remove the borders
        self.style.layout("Treeview", [('Treeview.treearea', {'sticky': 'news'})])
        # Creating the Table
        self.table = Treeview(root, column=col,
                              height=height, show='headings', style='Treeview')
        self.table.grid(row=row, column=column, sticky="news", padx=12)
        # Creating scroll bar for the table
        self.scroll = Scrollbar(root, orient='vertical', command=self.table.yview)
        self.scroll.grid(row=row, column=column, sticky='nes', padx=12)
        # Adding the scroll bar to the table
        self.table.configure(yscrollcommand=self.scroll.set)
        # First column/ID width
        for item in range(len(fields)):
            if item == 0:
                self.table.column(item, width=30)
            self.table.heading(item, text=fields[item], anchor='nw')
        # Populating the table with database rows
        for row_ in lst:
            self.table.insert('', 'end', values=" ".join(str(i).strip("\'") for i in row_))
