#!/usr/bin/python
from settings import *
from strings import *
from datetime import datetime

import MySQLdb


def connectDb():
    # create DB connection
    con = MySQLdb.connect(Settings().DBhost, Settings().DBuser,
                          Settings().DBpass, Settings().DBname)
    return con


def verify(userId):
    # create DB connection
    con = connectDb()
    cur = con.cursor()

    # Get student corresponding to the submitted line id
    qry = "SELECT id FROM student WHERE lineid='" + userId + "' AND active=1"
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


def usageLog(studentId, activityId):
    # create DB connection
    con = connectDb()
    cur = con.cursor()

    now = str(datetime.now())
    sql = "INSERT INTO usagelog (student, activity, timestamp) VALUES(" + str(studentId) + ", " + str(activityId) + ", '" + now + "')"
    cur.execute(sql)
    con.commit()
    con.close()


def register(authCode, userId):
    # check if alreadey registered
    studentId = verify(userId)
    if studentId == 0:
        # student have not registered yet

        con = connectDb()
        cur = con.cursor()

        # search for matching authentication code
        qry = "SELECT id, lineid FROM student WHERE authcode=" + authCode + " AND active=1"
        cur.execute(qry)
        # contain fetch result in array variable
        row = cur.fetchall()

        # check if there is a record with matching authcode
        if len(row) == 0:
            # no matching lineid
            result = Strings().REG_INVALID
        elif len(row) == 1:
            # there is 1 match, check if lineid is empty (not registered before)
            if row[0][1] == "":
                # add user lineid to database
                sql = "UPDATE student set lineid='" + str(userId) + "' WHERE id=" + str(row[0][0])
                cur.execute(sql)
                con.commit()
                # close connection
                con.close()

                result = Strings().REG_SUCCESS
                # record register activity
                usageLog(studentId, 1)
            else:
                result = Strings().REG_EXPIRED
        else:
            # other errors
            result = Strings().REG_FAILED
    # duplicate student or other errors
    elif studentId == -1:
        # exception error
        return Strings().ERR_FATAL
    else:
        # found matching student, already registered
        return Strings().REG_ALREADY

    return result


def today(userId):
    studentId = verify(userId)
    # determine which day is today
    # 0=monday, 6=sunday
    today = datetime.now().weekday()

    # sync day variable so 0=sunday and 5=saturday
    if today == 6:
        today = 0
    else:
        today += 1

    # student not registered
    if studentId == 0:
        return Strings().UNREG
    # duplicate student or other errors
    elif studentId == -1:
        return Strings().ERR_FATAL
    else:
        # create DB connection
        con = connectDb()
        cur = con.cursor()

        # fetch today's classes
        qry = "SELECT cr.name, cr.code, c.startclass, c.endclass, r.name AS building FROM takencourse t, course cr, class c, room r WHERE t.course=cr.id AND c.course=cr.id AND c.room=r.id AND c.day=" + str(today) + " AND c.active=1 AND t.student=" + str(studentId) + " ORDER BY c.startclass"
        print(qry)
        cur.execute(qry)
        # contain fetch result in array variable
        data = cur.fetchall()
        if len(data) > 0:
            # print header
            result = Strings().TODAY_HEADER
            # arranging query data so it displayed nicely
            for row in data:
                result += str(row[1]) + " " + str(row[0]) + "\n"
                result += str(row[2]) + " - " + str(row[3]) + "\n"
                result += str(row[4]) + "\n\n"
            # close connection
            con.close()
            # record activity
            usageLog(studentId, 2)
        else:
            result = Strings().TODAY_EMPTY

        return result


def checkroom(roomId, userId):
    # create DB connection
    con = connectDb()
    cur = con.cursor()
    # Get student corresponding to the submitted line id
    qry = "SELECT cr.name, cr.code, c.startclass, c.endclass, l.name AS lecturer FROM room r, course cr, class c, lecturer l WHERE c.room=r.id AND c.course=cr.id AND cr.lecturer=l.id AND r.id LIKE '%" + roomId + "%' AND c.active=1 ORDER BY c.startclass"
    cur.execute(qry)
    # contain fetch result in array variable
    data = cur.fetchall()
    print(data)
    print(len(data))
    if len(data) > 0:
        # print header
        result = Strings().ROOM_HEADER
        # arranging query data so it displayed nicely
        for row in data:
            result += str(row[1]) + " " + str(row[0]) + "\n"
            result += str(row[2]) + " - " + str(row[3]) + "\n"
            result += str(row[4]) + "\n\n"
        # close connection
        con.close()
        # record activity
        # usageLog(studentId, 2)
    else:
        result = Strings().ROOM_EMPTY
    return result


def schedule(userId):
    # contain returned studentId
    studentId = verify(userId)

    # student not registered
    if studentId == 0:
        return Strings().UNREG
    # duplicate student or other errors
    elif studentId == -1:
        return Strings().ERR_FATAL
    else:
        # create DB connection
        con = connectDb()
        cur = con.cursor()
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
        # record activity
        usageLog(studentId, 3)
        return result
