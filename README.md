# Taxi_Booking_System
## University Year 1 Second semester Final Project/Assignment 2
This application is built to demonstrate the knowledge of learned material in semester 2 of Year 1.
The application is built:

`PyCharm 2018.3.3 (Professional Edition)
Build #PY-183.5153.39, built on January 9, 2019
Licensed to Oszkar Feher
Subscription is active until February 13, 2021
For educational use only.
JRE: 1.8.0_152-release-1343-b26 amd64
JVM: OpenJDK 64-Bit Server VM by JetBrains s.r.o
Windows 10 10.0`

Main language: 

`python` version `3.6`.

Libraries: 

`tkinter` built in library - for graphical user interface (GUI)

`peewee` version `3.5.0` - object relational mapper (ORM) to handle database

`werkzeug` version `1.0.1` - to hash input passwords

All other relevant libraries can be found in 

`requirements.txt`

It's based on fictional Taxi booking system where customers, drivers and app administrator 
can interact on a GUI.
Each user type is limited to a certain interaction with the application, dependent on
the level of user status.

#### User types:
**`User`** 
- can register;
- book a trip by giving distance in miles;
- cancel booked trip.

**`Driver`** 
- can register and to view total income and distance driven.

**`Admin`** 
- can register only on code level and not inside the application;
- can view all booked trips, confirming a booked trip automatically allocating a driver for it;
- can view User or Driver full information;
- can delete an unconfirmed trip or past/finished trip;
- can delete a Driver or User.

All user types can log out.

## For start,
Create virtual environment and install all requirements with fooling command:

`pip install requirements.txt`

The database is populated with 5 users, 5 drivers and 1 admin,
all credentials are on `populate_db.py`.

After all installations run `booking_system.py` and will start the application. 

### Requirements
`requirements.txt`, python `3.6+`
