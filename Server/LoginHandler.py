import os
import sys
import json
import time
import requests
import tornado.ioloop
import tornado.web
import tornado.websocket
import logging
import sqlite3
from URIParser import *

database_dir = "C:\\databases"
users_db = os.path.join(database_dir, "users.db")

# /auth/username=name;password=pass
class LoginHandler(tornado.web.RequestHandler):
    def get(self, creds):
        self.set_header("Access-Control-Allow-Origin", "*")
        logging.info("GET /auth")
        print ("Received creds" + creds)
        global users_db
        uriparser = URIParser()
        r = uriparser.parse(creds)['dict']
        status = ''
        conn = sqlite3.connect(users_db)

        if conn is not None:
            q = "SELECT id FROM users WHERE username='%s' AND password='%s';" % (r['username'],r['password'])
            print (q)
            cursor  = conn.cursor().execute(q)
            if (cursor.fetchone()):
                status = "success"
            else:
                status = "invalid"
        else:
            status = 'error connecting to db or database does not exist'
        self.write({'status' : status})
