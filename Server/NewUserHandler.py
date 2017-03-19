import os
import sys
import json
import tornado.ioloop
import tornado.web
import logging
import sqlite3
from URIParser import *

database = "G:\\SachinK\progs\sqlite3\databases\library.db";
create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id INTEGER PRIMARY KEY,
                                        name text NOT NULL,
                                        password text NOT NULL
                                    ); """
                                    
# /newuser/username=name;password=pass
class NewUserHandler(tornado.web.RequestHandler):
    def post(self, creds):
        self.set_header("Access-Control-Allow-Origin", "*")
        global database
        global create_users_table
        print ("Received creds " + creds)
        uriparser = URIParser()
        r = uriparser.parse(creds)
        status = ''
        conn = sqlite3.connect(database)

        if conn is not None:
            conn.cursor().execute(create_users_table)
            q = "SELECT id FROM users WHERE name='%s' AND password='%s';" % (r['dict']['name'],r['dict']['password'])
            print (q)
            cursor  = conn.cursor().execute(q)
            if (cursor.fetchone()):
                status = 'exists'
                print ('User exists')
            else:
                print ("Adding user")
                q = "INSERT INTO users (name, password) VALUES ('%s', '%s');" % (r['dict']['name'],r['dict']['password'])
                print (q)
                conn.cursor().execute(q)
                conn.commit()
                status = 'added'
        else:
            status = 'error connecting to db'
        self.write({'status' : status})

