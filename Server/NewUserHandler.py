import os
import sys
import json
import tornado.ioloop
import tornado.web
import logging
import sqlite3
from URIParser import *

database_dir = "C:\\databases"
users_db = os.path.join(database_dir, "users.db")
create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id INTEGER PRIMARY KEY,
                                        username text NOT NULL,
                                        password text NOT NULL
                        ); """

# /newuser/username=name;password=pass
class NewUserHandler(tornado.web.RequestHandler):
    def post(self, creds):
        self.set_header("Access-Control-Allow-Origin", "*")
        print ("Received creds " + creds)
        global users_db
        uriparser = URIParser()
        r = uriparser.parse(creds)['dict']
        status = ''
        conn = sqlite3.connect(users_db) #this will create the database if it does not exist
        if conn is not None:
            conn.cursor().execute(create_users_table)
            q = "SELECT id FROM users WHERE username='%s' AND password='%s';" % (r['username'],r['password'])
            print (q)
            cursor  = conn.cursor().execute(q)
            if (cursor.fetchone()):
                status = 'exists'
            else:
                self._addUser(conn, r) # adding to users db
                status = 'added'
        else:
            status = 'error connecting to db'
        self.write({'status' : status})
    
    def _addUser(self, conn, r):
        print ("Adding user")
        q = "INSERT INTO users (username, password) VALUES ('%s', '%s');" % (r['username'],r['password'])
        print (q)
        conn.cursor().execute(q)
        conn.commit()
        self._createUserDB(r) # create db, tables for user

    def _createUserDB(self, r):
        global database_dir
        user_dir = os.path.join(database_dir, r['username'])
        os.mkdir(user_dir)
        user_db = os.path.join(user_dir, "%s.db" % r['username'])
        
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
        conn.commit()

