#!/usr/bin/python
from settings import *

import MySQLdb


class Functions:
    def __init__(self):
        # create DB connection
        self.db = MySQLdb.connect(Settings().DBhost, Settings().DBuser,
                                  Settings().DBpass, Settings().DBname)
        # create cursor for query data execution
        self.cur = db.cursor()

    def selUser():
        # Use all the SQL you like
        cur.execute("SELECT * FROM faculty")

        # print all the first cell of all the rows
        for row in cur.fetchall():
            content = row[0]

        db.close()
        return content

    def today():
        # SQL statement
        qry = "SELECT cr.name, cr.code, c.startclass, c.endclass, r.name AS building FROM takencourse t, course cr, class c, room r WHERE t.course=cr.id AND c.course=cr.id AND c.room=r.id AND c.day=today AND c.active=1 AND t.student=1 ORDER BY c.startclass"

        # Use all the SQL you like
        cur.execute(qry)

        # print all the first cell of all the rows
        result="Today's schedule:\n"
        for row in cur.fetchall():
            result + = row[0] + row[1] + row[2] + row[3] + row[4] + "\n"

        db.close()
        return result
