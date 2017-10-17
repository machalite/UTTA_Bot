#!/usr/bin/python
from settings import *
from strings import *

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
        for x in range(len(row)):
            result += str(row[x])
        result += "\n"

    # close connection
    con.close()
    return content


def today():
    # create DB connection
    con = MySQLdb.connect(Settings().DBhost, Settings().DBuser,
                          Settings().DBpass, Settings().DBname)

    # create cursor for query data execution
    cur = con.cursor()

    # fetch today's classes
    qry = "SELECT cr.name, cr.code, c.startclass, c.endclass, r.name AS building FROM takencourse t, course cr, class c, room r WHERE t.course=cr.id AND c.course=cr.id AND c.room=r.id AND c.day=1 AND c.active=1 AND t.student=1 ORDER BY c.startclass"

    # Use all the SQL you like
    cur.execute(qry)

    # print all the first cell of all the rows
    result = "Today's schedule:\n"

    # arranging query so it displayed nicely
    for row in cur.fetchall():
        result += str(row[1])+" "+str(row[0])+"\n"
        result += str(row[2])+" - "+str(row[3])+"\n"
        result += str(row[4])+"\n\n"

    # close connection
    con.close()
    return result


def verify(id):
    # create DB connection
    con = MySQLdb.connect(Settings().DBhost, Settings().DBuser,
                          Settings().DBpass, Settings().DBname)

    # create cursor for query data execution
    cur = con.cursor()

    # Get student corresponding to the submitted line id
    qry = "SELECT id, name FROM student WHERE lineid=" + id

    cur.execute(qry)
    # contain fetch result in array variable
    row = cur.fetchall()

    # check if there is a student with matching lineid
    if len(row) == 0:
        # no matching lineid
        result = 0
    elif len(row) == 1:
        # there is 1 match, get the student id
        result = row[0]
    else:
        # other errors
        result = -1

    # close connection
    con.close()
    return result
