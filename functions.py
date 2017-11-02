from settings import *
from strings import *
from datetime import datetime

import MySQLdb
import pytz
import time


# def timeFormat(time):
#     time = str(time)
#     hour = time[0:2]
#     minute = time[3:5]
#     newTime = hour + "." + minute
#     return newTime

def timeDeltaFormat(time):
    time = time.total_seconds()
    hour, remainder = divmod(time, 3600)
    minute, second = divmod(remainder, 60)
    strTime = '%s.%s' % (hour, minute)
    return strTime


def connectDb():
    # to create connection to the database

    con = MySQLdb.connect(Settings().DB_HOST, Settings().DB_USER,
                          Settings().DB_PASS, Settings().DB_NAME)
    return con


def verify(userId):
    # to check if user's Line ID already registered in the database or not

    # create DB connection
    con = connectDb()
    cur = con.cursor()

    # Get student corresponding to the submitted Line ID

    qry = "SELECT id FROM student WHERE lineid='" + userId + "' AND active=1"
    cur.execute(qry)
    data = cur.fetchall()
    recAmount = len(data)

    # check if there is a student with matching Line ID
    if recAmount == 0:  # no matching Line ID
        result = 0  # not registered
    elif recAmount == 1:  # found a match
        studentId = str(data[0][0])
        result = studentId  # already registered. pass the student ID
    else:  # there are duplicate student records
        result = -1  # to signify fatal error

    con.close()  # close database connection
    return result


def usageLog(studentId, commandId):
    # to record user's request

    # create DB connection
    con = connectDb()
    cur = con.cursor()

    tz = pytz.timezone(Settings().TIME_ZONE)  # set time zone
    now = datetime.now(tz)  # get datetime with time zone

    # record user's request
    sql = "INSERT INTO usagelog (student, activity, timestamp) VALUES(" + str(studentId) + ", " + str(commandId) + ", '" + str(now) + "')"
    cur.execute(sql)
    con.commit()  # commit changes
    con.close()  # close database connection


def register(authCode, userId):
    # to register user's Line ID in the database

    studentId = verify(userId)  # check if already registered

    if studentId == 0:  # student have not registered yet

        # userId registration

        con = connectDb()
        cur = con.cursor()

        # search for student record by matching authentication code

        qry = "SELECT id, lineid FROM student WHERE authcode='" + authCode + "' AND active=1"
        cur.execute(qry)
        data = cur.fetchall()

        recAmount = len(data)  # get amount of record

        # check if there is a record with matching authcode

        if recAmount == 0:  # no matching lineid
            result = Strings().REG_INVALID
        elif recAmount == 1:  # found 1 matching lineid

            recLineId = data[0][1]  # get record lineId
            recId = str(data[0][0])  # get record ID

            # check if there is line ID

            if recLineId == "":  # no line ID, not registered
                # add user's line ID to database
                sql = "UPDATE student SET lineid='" + str(userId) + "' WHERE id=" + recId
                cur.execute(sql)
                con.commit()  # commit changes

                result = Strings().REG_SUCCESS # returns success message
                usageLog(recId, 1)  # record register activity
            else:
                result = Strings().REG_EXPIRED  # returns expired auth code message
        else:
            # other errors, multiple student with same line ID
            result = Strings().REG_FAILED  # returns failed registration message
    elif studentId == -1:
        return Strings().ERR_FATAL  # returns fatal error message
    else:
        # found matching student, already registered
        return Strings().REG_ALREADY  # returns already registered message

    con.close()  # close database connection
    return result


def today(userId):
    # check if already registered
    studentId = verify(userId)

    # get timezone
    tz = pytz.timezone(Settings().TIME_ZONE)

    # determine which day is today
    # 0=monday, 6=sunday
    today = datetime.now(tz).weekday()

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

        # get today's classes
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
                startTime = row[2]
                startTime = startTime.strftime("%H:%M")
                endTime = row[3]
                endTime = endTime.strftime("%H:%M")
                # startTime = time.strftime("%H:%M", row[2])  # time formatting
                # endTime = time.strftime("%H:%M", row[3])

                result += str(row[1]) + " " + str(row[0]) + "\n"
                result += str(startTime) + " - " + str(endTime) + "\n"
                result += str(row[4]) + "\n\n"
        else:
            result = Strings().TODAY_EMPTY

        # record activity
        usageLog(studentId, 2)

    # close connection
    con.close()
    return result


def checkroom(roomInput, userId):
    # create DB connection
    con = connectDb()
    cur = con.cursor()

    # check validity of submitted roomcode/roomname
    qry = "SELECT id FROM room WHERE name LIKE '%" + roomInput + "%' OR code='" + roomInput + "' AND active=1"
    cur.execute(qry)
    # contain fetch result in array variable
    data = cur.fetchall()
    if len(data) > 0:
        roomId = data[0][0]

        # get time with timezone
        tz = pytz.timezone(Settings().TIME_ZONE)

        # determine which day is today
        # 0=monday, 6=sunday
        today = datetime.now(tz).weekday()

        # sync day variable so 0=sunday and 5=saturday
        if today == 6:
            today = 0
        else:
            today += 1

        # get classes for submitted room id
        qry = "SELECT cr.name, cr.code, c.startclass, c.endclass, c.day, l.name AS lecturer, r.name AS room FROM room r, course cr, class c, lecturer l WHERE c.room=r.id AND c.course=cr.id AND cr.lecturer=l.id AND r.id=" + str(roomId) + " AND c.day=" + str(today) + " AND c.active=1 ORDER BY c.startclass"
        cur.execute(qry)
        # contain fetch result in array variable
        data = cur.fetchall()
        if len(data) > 0:
            # print header
            result = Strings().ROOM_HEADER + str(data[0][6]) + "\n\n"  # print room name
            # arranging query data so it displayed nicely
            for row in data:
                startTime = time.strftime("%H%M", row[2])  # time formatting
                endTime = time.strftime("%H%M", row[3])

                result += str(row[1]) + " " + str(row[0]) + "\n"
                result += str(startTime) + " - " + str(endTime) + "\n"
                result += str(row[5]) + "\n\n"
        else:
            result = Strings().ROOM_EMPTY

        # check if already registered
        studentId = verify(userId)
        if studentId == 0:
            # user not registered, record as anonymous
            usageLog(1, 3)
        else:
            # user already registered, record user activity
            usageLog(studentId, 3)
    else:
        result = Strings().ROOM_UNREG

    # close connection
    con.close()
    return result


def schedule(userId):
    # check if already registered
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

        # Get weekly schedule
        qry = "SELECT cr.name, cr.code, c.startclass, c.day FROM takencourse t, course cr, class c WHERE t.course=cr.id AND c.course=cr.id AND t.student=" + studentId + " AND c.active=1 ORDER BY c.day, c.startclass"
        cur.execute(qry)

        data = cur.fetchall()
        if len(data) > 0:
            # print header
            result = Strings().SCHEDULE_HEADER + "\n"

            # determine day name
            curDay = 0
            for row in data:
                if row[3] == 1:
                    txtDay = Strings().SCHEDULE_MON
                elif row[3] == 2:
                    txtDay = Strings().SCHEDULE_TUE
                elif row[3] == 3:
                    txtDay = Strings().SCHEDULE_WED
                elif row[3] == 4:
                    txtDay = Strings().SCHEDULE_THU
                elif row[3] == 5:
                    txtDay = Strings().SCHEDULE_FRI
                elif row[3] == 6:
                    txtDay = Strings().SCHEDULE_SAT
                else:
                    txtDay = Strings().SCHEDULE_SUN

                # print day name
                if row[3] != curDay:
                    result += "\n" + txtDay + "\n"
                    curDay = row[3]

                startTime = timeDeltaFormat(row[2])

                # arranging query result so it displayed nicely
                result += startTime + " " + str(row[0]) + "\n"
        else:
            result = Strings().SCHEDULE_EMPTY

        # record activity
        usageLog(studentId, 4)

    # close connection
    con.close()
    return result


def next(userId):
    # check if already registered
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

        # get time with timezone
        tz = pytz.timezone(Settings().TIME_ZONE)
        now = datetime.now(tz)

        # determine which day is today
        # 0=monday, 6=sunday
        today = datetime.now(tz).weekday()

        # sync day variable so 0=sunday and 5=saturday
        if today == 6:
            today = 0
        else:
            today += 1

        # Get next class
        qry = "SELECT cr.name, cr.code, c.startclass, c.endclass, l.name AS lecturer, r.name AS room FROM takencourse t, course cr, class c, room r, lecturer l WHERE t.course=cr.id AND c.course=cr.id AND cr.lecturer=l.id AND c.room=r.id AND c.startclass<'" + str(now) + "' AND c.day=" + str(today) + " AND c.active=1 AND t.student=" + str(studentId) + " ORDER BY c.startclass LIMIT 1"
        cur.execute(qry)
        data = cur.fetchall()

        if len(data) > 0:
            # print header
            result = Strings().NEXT_HEADER + "\n"
            for row in data:
                # arranging query result so it displayed nicely
                result += str(row[1]) + " " + str(row[0]) + "\n"
                result += str(row[2]) + " - " + str(row[3]) + "\n"
                result += str(row[5]) + "\n"
                result += str(row[4]) + "\n"
        else:
            result = Strings().NEXT_NOCLASS

        # record activity
        usageLog(studentId, 5)

    # close connection
    con.close()
    return result


def where(roomInput, userId):
    # create DB connection
    con = connectDb()
    cur = con.cursor()

    # get room information
    qry = "SELECT r.floor, r.code, r.name, r.description, b.name AS building, b.description AS buildingDesc FROM building b, room r WHERE r.building=b.id AND r.id=(SELECT id FROM room WHERE name LIKE '%" + roomInput + "%' OR code='" + roomInput + "' AND active=1)"
    cur.execute(qry)
    # contain fetch result in array variable
    data = cur.fetchall()
    result = ""
    if len(data) > 0:
        for row in data:
            result += str(row[1]) + " " + str(row[2]) + "\n"
            result += str(row[3]) + "\n"
            result += str(row[4]) + " " + Strings().WHERE_FLOOR + " " + str(row[0]) + "\n"
            result += str(row[5]) + "\n\n"

        # check if already registered
        studentId = verify(userId)
        if studentId == 0:
            # user not registered, record as anonymous
            usageLog(1, 6)
        else:
            # user already registered, record user activity
            usageLog(studentId, 6)
    else:
        result = Strings().ROOM_UNREG

    # close connection
    con.close()
    return result


def checkcourse(courseInput, userId):
    # create DB connection
    con = connectDb()
    cur = con.cursor()

    # check validity of submitted course code
    qry = "SELECT cr.id, cr.name, cr.code, l.name AS lecturer FROM course cr, lecturer l WHERE cr.lecturer=l.id AND cr.code LIKE '%" + courseInput + "%' AND cr.active=1"
    cur.execute(qry)
    # contain fetch result in array variable
    data = cur.fetchall()
    if len(data) > 0:
        courseId = data[0][0]
        # display message header
        result = data[0][2] + " " + data[0][1] + "\n"  # print course code and name
        result += data[0][3] + "\n"  # print lecturer name

        # get list of classes
        qry = "SELECT c.startclass, c.endclass, c.day, r.name AS room FROM course cr, class c, room r WHERE cr.id=" + str(courseId) + " AND c.course=cr.id AND c.room=r.id AND cr.active=1 ORDER BY c.day, c.startclass"
        cur.execute(qry)
        # contain fetch result in array variable
        data = cur.fetchall()

        if len(data) > 0:
            curDay = 0
            for row in data:
                # determine day name
                if row[2] == 1:
                    txtDay = Strings().SCHEDULE_MON
                elif row[2] == 2:
                    txtDay = Strings().SCHEDULE_TUE
                elif row[2] == 3:
                    txtDay = Strings().SCHEDULE_WED
                elif row[2] == 4:
                    txtDay = Strings().SCHEDULE_THU
                elif row[2] == 5:
                    txtDay = Strings().SCHEDULE_FRI
                elif row[2] == 6:
                    txtDay = Strings().SCHEDULE_SAT
                else:
                    txtDay = Strings().SCHEDULE_SUN

                # print day name
                if row[2] != curDay:
                    result += "\n" + txtDay + "\n"
                    curDay = row[2]

                # arranging query result so it displayed nicely
                result += str(row[0]) + " - " + str(row[1]) +  "\n"
                result += str(row[3]) + "\n"

            # check if already registered
            studentId = verify(userId)
            if studentId == 0:
                # user not registered, record as anonymous
                usageLog(1, 7)
            else:
                # user already registered, record user activity
                usageLog(studentId, 7)

        else:
            result = Strings().COURSE_NOCLASS
    else:
        result = Strings().COURSE_INVALID

    # close connection
    con.close()
    return result


def changes(userId):
    # check if already registered
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

        # get time with timezone
        tz = pytz.timezone(Settings().TIME_ZONE)
        now = datetime.now(tz)

        # Get schedule changes information
        qry = "SELECT cr.name, cr.code, o.status, o.startclass, o.endclass, o.description, o.date, r.name AS room FROM offclass o, takencourse t, class c, course cr, room r WHERE t.course=cr.id AND c.course=cr.id AND o.room=r.id AND o.class=c.id AND t.student=" + str(studentId) + " AND o.date>'" + str(now) + "' AND o.active=1 ORDER BY o.date, o.startclass"
        cur.execute(qry)
        data = cur.fetchall()

        if len(data) > 0:
            result = Strings().CHANGES_HEADER + "\n"

            # determine change status
            for row in data:
                if row[2] == 1:
                    txtStatus = Strings().CHANGES_CANCELLED
                elif row[2] == 2:
                    txtStatus = Strings().CHANGES_POSTPONED
                elif row[2] == 3:
                    txtStatus = Strings().CHANGES_RELOCATED
                elif row[2] == 4:
                    txtStatus = Strings().CHANGES_REPLACEMENT
                else:
                    txtStatus = Strings().CHANGES_SUPPLEMENTARY

                result += str(row[1]) + " " + str(row[0]) + "\n"  #print course code and name
                result += txtStatus + "\n"
                result += str(row[6]) + " " + str(row[3]) + " - " + str(row[4]) + "\n"
                result += str(row[7]) + "\n"
                result += str(row[5]) + "\n\n"

            # record user activity
            usageLog(studentId, 8)
        else:
            result = Strings().CHANGES_NOCHANGES

    # close connection
    con.close()
    return result
