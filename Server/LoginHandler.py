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
database = "G:\\SachinK\progs\sqlite3\databases\users.db";

# /auth/username=name;password=pass
class LoginHandler(tornado.web.RequestHandler):
    def get(self, creds):
        self.set_header("Access-Control-Allow-Origin", "*")
        logging.info("GET /auth")
        print ("Received creds" + creds)
        global database
        uriparser = URIParser()
        r = uriparser.parse(creds)
        status = ''
        conn = sqlite3.connect(database)

        if conn is not None:
            q = "SELECT id FROM users WHERE name='%s' AND password='%s';" % (r['dict']['name'],r['dict']['password'])
            print (q)
            cursor  = conn.cursor().execute(q)
            if (cursor.fetchone()):
                status = "success"
            else:
                status = "invalid"
        else:
            status = 'error connecting to db or database does not exist'
        self.write({'status' : status})
