#!/usr/bin/python
from settings import *

import MySQLdb


def selUser():
    # create DB connection
    con = MySQLdb.connect(Settings().DBhost, Settings().DBuser,
                          Settings().DBpass, Settings().DBname)

    # create cursor for query data execution
    cur = con.cursor()
    # Use all the SQL you like
    cur.execute("SELECT * FROM faculty")

    # print all the first cell of all the rows
    for row in cur.fetchall():
        content = row[0]

    # close connection
    con.close()
    return content


def today():
    # create DB connection
    con = MySQLdb.connect(Settings().DBhost, Settings().DBuser,
                          Settings().DBpass, Settings().DBname)

    # create cursor for query data execution
    cur = con.cursor()
    # SQL statement
    qry = "SELECT cr.name, cr.code, c.startclass, c.endclass, r.name AS building FROM takencourse t, course cr, class c, room r WHERE t.course=cr.id AND c.course=cr.id AND c.room=r.id AND c.day=1 AND c.active=1 AND t.student=1 ORDER BY c.startclass"

    # Use all the SQL you like
    cur.execute(qry)

    # print all the first cell of all the rows
    result = "Today's schedule:\n"

    for row in cur.fetchall():
        for x in row:
            result += str(row[x])
        result += "\n"

    # close connection
    con.close()
    return result
