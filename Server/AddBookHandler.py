import os
import sys
import uuid
import json
import tornado.ioloop
import tornado.web
import logging
import sqlite3
from URIParser import *

database_dir = "C:\\databases"

class AddBookHandler(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        #print (self.request.files)
        username = self.get_body_argument("username", default=None, strip=False)
        title = self.get_body_argument("title", default=None, strip=False)
        author = self.get_body_argument("author", default=None, strip=False)
        category = self.get_body_argument("category", default=None, strip=False)
        fileinfo = self.request.files['0'][0]
        filename = fileinfo['filename']
        extn = os.path.splitext(filename)[1]
        cname = str(uuid.uuid4()) + extn
        user_dir = os.path.join(database_dir, username)
        ofile = os.path.join(user_dir, cname)
        fh = open(ofile, 'wb')
        fh.write(fileinfo['body'])
        # finished saving image
        status = '';
        user_db = os.path.join(user_dir, "%s.db" % username)
        conn = sqlite3.connect(user_db)
        create_books_table = """ CREATE TABLE IF NOT EXISTS books (
                                        id INTEGER PRIMARY KEY,
                                        author TEXT NOT NULL,
                                        title TEXT NOT NULL,
                                        category TEXT NOT NULL,
                                        img_filename TEXT NOT NULL,
                                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                        ); """ 
        conn.cursor().execute(create_books_table)
        if conn is not None:
            q = "INSERT INTO books (title, author, category, img_filename) VALUES (?,?,?,?);"
            print (q)
            conn.cursor().execute(q,(title,author,category,cname))
            conn.commit()
            status = "OK"
        else:
            status = "NOK"
        self.finish({"status" : status})
