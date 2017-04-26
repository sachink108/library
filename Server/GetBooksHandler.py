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

class GetBooksHandler(tornado.web.RequestHandler):
    def get(self, info):
        self.set_header("Access-Control-Allow-Origin", "*")
        logging.info("GET /getbooks")
        global users_db
        global database_dir
        uriparser = URIParser()
        r = uriparser.parse(info)['dict']
        print ("Getting books for %s of category %s" %(r['user'], r['cat']))
        
        user_dir = os.path.join(database_dir, r['user'])
        user_db = os.path.join(user_dir, r['user'] + ".db")
        conn = sqlite3.connect(user_db)
        if (r['cat'] == 'recent'):
            q = "SELECT * FROM books ORDER BY timestamp DESC LIMIT 5";
        else:
            q = "SELECT * FROM books WHERE category='%s' ORDER BY timestamp DESC" % r['cat']
        cursor = conn.cursor().execute(q)
        ret = {}
        for row in cursor.fetchall():
            cat = row[3]
            if (cat not in ret):
                ret[cat] = []
            ret[cat].append( {"author" : row[1],
                              "title" : row[2],
                               "img": "%s/%s" % (r['user'],row[4]),
                              } )
        
        q = "SELECT category, count(*) FROM books GROUP BY category";
        cursor = conn.cursor().execute(q)
        catret = []
        for row in cursor.fetchall():
            catret.append({'name': row[0], 'count': row[1]})

        self.write({'books': ret,
                    'categories': catret})
        