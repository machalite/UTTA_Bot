#!/usr/bin/python
from settings import *

import MySQLdb


def selUser():
    db = MySQLdb.connect(host=Settings().DBhost,    # your host, usually localhost
                         user=Settings().DBuser,         # your username
                         passwd=Settings().DBpass,  # your password
                         db=Settings().DBname)        # name of the data base

    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor()

    # Use all the SQL you like
    cur.execute("SELECT * FROM user")

    # print all the first cell of all the rows
    for row in cur.fetchall():
        content = row[0]

    return content

    db.close()
