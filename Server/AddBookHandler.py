import os
import sys
import uuid
import json
import tornado.ioloop
import tornado.web
import logging
import sqlite3
from PIL import Image
import base64
from URIParser import *

database_dir = "C:\\databases"

class AddBookHandler(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        username = self.get_body_argument("username", default=None, strip=False)
        title = self.get_body_argument("title", default=None, strip=False)
        author = self.get_body_argument("author", default=None, strip=False)
        category = self.get_body_argument("category", default=None, strip=False)
        
        if (len(self.request.files.keys()) > 0):
            fileinfo = self.request.files['0'][0]
            filename = fileinfo['filename']
            extn = os.path.splitext(filename)[1]
            cname = str(uuid.uuid4()) + extn
            user_dir = os.path.join(database_dir, username)
            ofile = os.path.join(user_dir, cname)
            fh = open(ofile, 'wb')
            fh.write(fileinfo['body'])
            # finished saving image
        else:
            cname = str(uuid.uuid4()) + ".jpg"
            user_dir = os.path.join(database_dir, username)
            ofile = os.path.join(user_dir, cname)
            fh = open(ofile, 'wb')
            img_data = self.get_body_argument("0", default=None, strip=False)
            print (img_data)
            #img = base64.decodestring(img_data)
            img = base64.decodestring(bytes(img_data,'utf-8'))
            fh.write(img)
            
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
