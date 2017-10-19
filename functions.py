#!/usr/bin/python
from settings import *
from strings import *

import MySQLdb


def connectDb():
    # create DB connection
    con = MySQLdb.connect(Settings().DBhost, Settings().DBuser,
                          Settings().DBpass, Settings().DBname)
    return con


def selUser():
    # create DB connection
    con = connectDb()
    cur = con.cursor()

    cur.execute("SELECT * FROM faculty")

    # print all the first cell of all the rows
    for row in cur.fetchall():
        for x in range(len(row)):
            result += str(row[x])
        result += "\n"

    # close connection
    con.close()
    return result


def today():
    # create DB connection
    con = connectDb()
    cur = con.cursor()

    # fetch today's classes
    qry = "SELECT cr.name, cr.code, c.startclass, c.endclass, r.name AS building FROM takencourse t, course cr, class c, room r WHERE t.course=cr.id AND c.course=cr.id AND c.room=r.id AND c.day=1 AND c.active=1 AND t.student=1 ORDER BY c.startclass"
    cur.execute(qry)

    # print header
    result = Strings().TODAY_HEADER

    # arranging query so it displayed nicely
    for row in cur.fetchall():
        result += str(row[1])+" "+str(row[0])+"\n"
        result += str(row[2])+" - "+str(row[3])+"\n"
        result += str(row[4])+"\n\n"

    # close connection
    con.close()
    return result


def verify(userId):
    # create DB connection
    con = connectDb()
    cur = con.cursor()

    # Get student corresponding to the submitted line id
    qry = "SELECT id, name FROM student WHERE lineid='" + userId + "'"
    cur.execute(qry)
    # contain fetch result in array variable
    row = cur.fetchall()

    # check if there is a student with matching lineid
    if len(row) == 0:
        # no matching lineid
        result = 0
    elif len(row) == 1:
        # there is 1 match, get the student id
        result = str(row[0][0])
    else:
        # other errors
        result = -1

    # close connection
    con.close()
    return result


def schedule(userId):
    # create DB connection
    con = connectDb()
    cur = con.cursor()

    # contain returned studentId
    studentId = verify(userId)
    print(studentId)

    # student not registered
    if studentId == 0:
        return Strings().UNREG
    # duplicate student or other errors
    elif studentId == -1:
        return Strings().ERR_FATAL
    else:
        # Get student corresponding to the submitted line id
        qry = "SELECT cr.name, cr.code, c.startclass, c.day FROM takencourse t, course cr, class c WHERE t.course=cr.id AND c.course=cr.id AND t.student=" + studentId + " AND c.active=1 ORDER BY c.day, c.startclass"
        cur.execute(qry)
        # print header
        result = Strings().SCHEDULE_HEADER

        # arranging query so it displayed nicely
        for row in cur.fetchall():
            result += str(row[1])+" "+str(row[0])+" "+str(row[2])+"\n"

        # close connection
        con.close()
        return result


def register(authCode, userId):
    # create DB connection
    con = connectDb()
    cur = con.cursor()

    # search for matching authentication code
    qry = "SELECT id, name, lineid FROM student WHERE authcode='" + authCode + "'"
    cur.execute(qry)
    # contain fetch result in array variable
    row = cur.fetchall()

    # check if there is a record with matching authcode
    if len(row) == 0:
        # no matching lineid
        result = Strings().REG_INVALID
    elif len(row) == 1:
        # there is 1 match, check if lineid is empty (not registered before)
        if row[0][2] == "":
            sql = "UPDATE student set lineid='" + str(userId) + "' WHERE id=" + row[0][0]
            cur.execute(sql)
            result = Strings().REG_SUCCESS
        else:
            result = Strings().REG_EXPIRED
    else:
        # other errors
        result = Strings().REG_FAILED
    # close connection
    con.close()
    return result
